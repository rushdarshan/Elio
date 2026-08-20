# WALK_TEST — Fresh-Clone Acceptance Gate

**Bar:** R10 — a fresh agent with no project context can clone → run
verification → understand the claim → inspect evidence.

This is a checklist, not a script. Every item below is executed as-is from a
clean clone in a temp directory, on the target machine (no PowerShell
required for the core path; `python -B scripts\verify_everything.py` is
cross-platform).

## Checklist

1. **Clone the repo** into a fresh temp directory.
   ```bash
   git clone <repo-url> walk-test && cd walk-test
   ```
2. **Read README** — the gold claim, pipeline summary, and Verification
   section should be self-explanatory and internally consistent.
3. **Run verification** — expect ACCEPTED:
   ```bash
   python -B scripts\verify_everything.py
   ```
4. **Run manifest verify** — expect ALL PASS:
   ```bash
   python -B scripts\verify_manifest.py
   ```
5. **Open `demo.html`** (offline, from `file://`) and search `PDSH4816AF`:
   - one accepted value shows a WHY? trace with evidence snippet + confidence
   - one cell shows `[ABSTAINED]` with a reason (e.g. `PART_NUMBER`)
6. **Read `docs/PITCH.md`** — confirm the headline numbers match the
   verification output and `artifacts/metrics.json`.
7. **Time the whole thing** — target under 10 minutes from clean clone.

## Edge cases covered

- **No PowerShell:** the verification commands are plain `python -B ...`;
  no shell-specific syntax is required to run the acceptance gates.
- **Offline machine:** `demo.html` is fully self-contained (no external
  network references — enforced at build time by `build_demo_html.py`);
  manifest verification reads local files only.

## Run log

- **Date:** 2026-08-20
- **Environment:** Windows, Python 3.13.7, cloned from local mirror (`git clone`)
- **Outcome:** PASS — every checklist item passed; `verify_everything.py` → ACCEPTED, `verify_manifest.py` → ALL PASS, `demo.html` opened offline with 0 external refs, PDSH4816AF showed accepted Amperage "15 A" with evidence and `PART_NUMBER` `[ABSTAINED]` with reason
- **Elapsed time:** 5s (clone → verification → evidence inspection; well under the 10-minute target)
- **Failures / notes:** initial run failed manifest verify — root cause `core.autocrlf=true` (working tree LF vs fresh-clone CRLF bytes) plus an uncommitted manifest-bound origin-doc. Fixed by normalizing `\r\n` in `verify_manifest.py` hashing and committing the origin doc. Re-run passed clean. Commit `946b882`.