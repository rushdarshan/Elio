import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

const execAsync = promisify(exec);

// Limits for live web deployment
const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024; // 5 MB
const MAX_ROW_COUNT = 500; // Cap live web demo to 500 rows per upload
const RATE_LIMIT_WINDOW_MS = 60 * 1000; // 1 minute
const MAX_REQUESTS_PER_WINDOW = 15;
const MAX_CONCURRENT_JOBS = 2;

// In-memory rate limiter & concurrency tracker
const ipRequestHistory = new Map<string, number[]>();
let activeJobsCount = 0;

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const timestamps = (ipRequestHistory.get(ip) || []).filter(t => now - t < RATE_LIMIT_WINDOW_MS);
  if (timestamps.length >= MAX_REQUESTS_PER_WINDOW) {
    ipRequestHistory.set(ip, timestamps);
    return true;
  }
  timestamps.push(now);
  ipRequestHistory.set(ip, timestamps);
  return false;
}

export async function POST(request: NextRequest) {
  // Extract client IP for rate limiting
  const ip = request.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || '127.0.0.1';

  if (isRateLimited(ip)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded. Please wait a minute before running another batch.' },
      { status: 429 }
    );
  }

  if (activeJobsCount >= MAX_CONCURRENT_JOBS) {
    return NextResponse.json(
      { error: 'System is currently processing concurrent batches. Please retry in a few seconds.' },
      { status: 503 }
    );
  }

  activeJobsCount++;

  try {
    const formData = await request.formData();
    const file = formData.get('file') as File | null;

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded.' }, { status: 400 });
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      return NextResponse.json(
        { error: `File size exceeds ${MAX_FILE_SIZE_BYTES / (1024 * 1024)}MB limit.` },
        { status: 413 }
      );
    }

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // Enforce required columns validation (dry-run check)
    const csvContent = buffer.toString('utf-8');
    const firstLine = csvContent.split('\n')[0] || '';
    const headers = firstLine.split(',').map(h => h.replace(/^\ufeff/, '').replace(/"/g, '').trim());

    // Required columns
    const required = ['Mfg_Part_Num', 'Part_Desc', 'Part_Manuf', 'E1_Brand', 'Unilog_Brand', 'DIB_Brand'];
    const missing = required.filter(col => !headers.includes(col));

    // Fallback headers support (MPN, Description, Manufacturer)
    const fallbackRequired = ['MPN', 'Description', 'Manufacturer'];
    const hasFallback = fallbackRequired.every(col => headers.includes(col));

    if (missing.length > 0 && !hasFallback) {
      return NextResponse.json({
        error: `Missing required columns: ${missing.join(', ')} (or standard headers: MPN, Description, Manufacturer)`
      }, { status: 400 });
    }

    // Count rows
    const lines = csvContent.split('\n').filter(line => line.trim() !== '');
    const rowCount = lines.length > 1 ? lines.length - 1 : 0;
    if (rowCount < 1) {
      return NextResponse.json({ error: 'CSV must contain at least one data row.' }, { status: 400 });
    }

    if (rowCount > MAX_ROW_COUNT) {
      return NextResponse.json({
        error: `Uploaded file has ${rowCount} rows. Live browser demo is capped at ${MAX_ROW_COUNT} rows per batch. Use the CLI runner for larger datasets.`
      }, { status: 400 });
    }

    // Generate SHA-256 hash of the input file
    const hash = crypto.createHash('sha256').update(buffer).digest('hex');

    // Resolve project root dynamically (handles both cwd in elio-frontend and root)
    let projectRoot = process.cwd();
    if (!fs.existsSync(path.join(projectRoot, 'unihack_catalog'))) {
      const parent = path.resolve(projectRoot, '..');
      if (fs.existsSync(path.join(parent, 'unihack_catalog'))) {
        projectRoot = parent;
      }
    }

    // Create temporary file paths in projectRoot/tmp
    const tempDir = path.join(projectRoot, 'tmp');
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }

    const uniqueId = crypto.randomBytes(8).toString('hex');
    const tempInputPath = path.join(tempDir, `input_${uniqueId}.csv`);
    const tempOutputPath = path.join(tempDir, `output_${uniqueId}.json`);

    // Write input file to disk
    fs.writeFileSync(tempInputPath, buffer);

    const pythonScript = path.join(projectRoot, 'scripts', 'run_pipeline_cli.py');
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    const command = `"${pythonCmd}" -B "${pythonScript}" --input "${tempInputPath}" --output "${tempOutputPath}"`;

    await execAsync(command, { cwd: projectRoot, timeout: 120_000, maxBuffer: 20 * 1024 * 1024 });

    // Read pipeline results JSON
    if (!fs.existsSync(tempOutputPath)) {
      return NextResponse.json({ error: 'Pipeline run failed to produce output file.' }, { status: 500 });
    }

    const rawResults = fs.readFileSync(tempOutputPath, 'utf-8');
    const results = JSON.parse(rawResults);
    if (!Array.isArray(results) || results.length !== rowCount) {
      return NextResponse.json({ error: `Pipeline processed ${Array.isArray(results) ? results.length : 0} of ${rowCount} rows.` }, { status: 502 });
    }

    // Clean up temporary files
    try {
      if (fs.existsSync(tempInputPath)) fs.unlinkSync(tempInputPath);
      if (fs.existsSync(tempOutputPath)) fs.unlinkSync(tempOutputPath);
    } catch (e) {
      console.error('Error cleaning up temp files:', e);
    }

    return NextResponse.json({
      hash,
      rowCount,
      results
    });
  } catch (error: any) {
    console.error('Pipeline API Route Error:', error);
    // Sanitize error messages in production to avoid leaking server internals
    const isDev = process.env.NODE_ENV === 'development';
    return NextResponse.json({
      error: 'An error occurred during pipeline execution.',
      details: isDev ? (error?.message || String(error)) : 'Internal processing error'
    }, { status: 500 });
  } finally {
    activeJobsCount = Math.max(0, activeJobsCount - 1);
  }
}
