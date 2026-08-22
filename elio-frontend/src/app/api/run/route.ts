import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File | null;

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
    }

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // Enforce 6 required columns validation (dry-run check)
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
        error: `Missing required columns: ${missing.join(', ')}`
      }, { status: 400 });
    }

    // Generate SHA-256 hash of the input file
    const hash = crypto.createHash('sha256').update(buffer).digest('hex');

    // Create temporary file paths
    const tempDir = path.join(process.cwd(), 'tmp');
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }

    const uniqueId = crypto.randomBytes(8).toString('hex');
    const tempInputPath = path.join(tempDir, `input_${uniqueId}.csv`);
    const tempOutputPath = path.join(tempDir, `output_${uniqueId}.json`);

    // Write input file to disk
    fs.writeFileSync(tempInputPath, buffer);

    // Count rows
    const lines = csvContent.split('\n').filter(line => line.trim() !== '');
    const rowCount = lines.length > 1 ? lines.length - 1 : 0;
    if (rowCount < 1) {
      return NextResponse.json({ error: 'CSV must contain at least one data row' }, { status: 400 });
    }

    // Resolve parent directory where app.py and unihack_catalog live
    const parentDir = path.resolve(process.cwd(), '..');
    const pythonScript = path.join(parentDir, 'scripts/run_pipeline_cli.py');

    // Run python pipeline script
    // Ensure we use the correct virtual environment Python or fallback to global python
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    const command = `"${pythonCmd}" "${pythonScript}" --input "${tempInputPath}" --output "${tempOutputPath}"`;

    console.log(`Running command: ${command}`);
    await execAsync(command, { cwd: parentDir, timeout: 120_000, maxBuffer: 10 * 1024 * 1024 });

    // Read pipeline results JSON
    if (!fs.existsSync(tempOutputPath)) {
      return NextResponse.json({ error: 'Pipeline run failed to write results' }, { status: 500 });
    }

    const rawResults = fs.readFileSync(tempOutputPath, 'utf-8');
    const results = JSON.parse(rawResults);
    if (!Array.isArray(results) || results.length !== rowCount) {
      return NextResponse.json({ error: `Pipeline returned ${Array.isArray(results) ? results.length : 0} of ${rowCount} rows` }, { status: 502 });
    }

    // Clean up temporary files
    try {
      fs.unlinkSync(tempInputPath);
      fs.unlinkSync(tempOutputPath);
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
    return NextResponse.json({
      error: 'An internal error occurred during pipeline execution.',
      details: error.message || error
    }, { status: 500 });
  }
}
