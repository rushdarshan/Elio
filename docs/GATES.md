# Gates: Judge-Proof Uni-Hack Submission

Scope: verify ELIO against the organizers' real contract and live evaluator workflow without changing the frozen pipeline.

- [x] G1: Official input and expected-output files exist and share the required 252-column contract.
  CHECK: python -B -c "import csv, pathlib; inp=pathlib.Path('Unihack_ Sample Dataset - Input.csv'); out=pathlib.Path('Unihack_ Expected Output - Delivery Format.csv'); assert inp.exists() and out.exists(); h=list(csv.reader(out.open(encoding='utf-8-sig')))[0]; assert len(h)==252, len(h); print(f'OFFICIAL_FILES_PASS headers={len(h)} input={inp.stat().st_size} output={out.stat().st_size}')"
  EXPECT: OFFICIAL_FILES_PASS headers=252
  EVIDENCE: OFFICIAL_FILES_PASS headers=252 input=128673 output=8695

- [x] G2: Frozen Bar-5 clean pipeline remains intact, with zero answer-key hardcoding.
  CHECK: python -B -c "import subprocess,sys; r=subprocess.run([sys.executable,'-B','scripts/check_freeze.py'],capture_output=True,text=True); assert r.returncode==0, r.stdout+r.stderr; print('FREEZE_GATE_PASS')"
  EXPECT: FREEZE_GATE_PASS
  EVIDENCE: FREEZE_GATE_PASS

- [x] G3: Canonical verification reports honest gold, export, dual-pass, and holdout results.
  CHECK: python -B scripts/verify_everything.py
  EXPECT: VERDICT: ACCEPTED
  EVIDENCE: VERDICT: ACCEPTED

- [x] G4: Submission manifest binds every shipped artifact without drift.
  CHECK: python -B scripts/verify_manifest.py
  EXPECT: ALL PASS
  EVIDENCE: MANIFEST VERIFY: ALL PASS

- [x] G5: Content-addressed receipts reject mutations rather than reporting hardcoded success.
  CHECK: python -B scripts/test_receipt.py
  EXPECT: receipt mutation checks: input/source/decision/output tamper rejected
  EVIDENCE: [PASS] receipt mutation checks: input/source/decision/output tamper rejected

- [x] G6: Artifact and live cockpit judge walks exercise upload, evidence, review, abstention, export, and proof verification.
  CHECK: python -B scripts/judge_walk.py --live
  EXPECT: JUDGE_WALK_STATUS: VERIFIED + live cockpit
  EVIDENCE: [PASS] live upload verified: 50 rows | JUDGE_WALK_STATUS: VERIFIED + live cockpit

- [x] G7: Frontend typecheck and production build pass.
  CHECK: npm --prefix elio-frontend run build
  EXPECT: ✓ Compiled successfully
  EVIDENCE: ✓ Compiled successfully; production build exited 0

- [x] G8: A fresh evaluator CSV reaches the real API and produces a non-empty, correctly shaped result.
  CHECK: python -B scripts/judge_walk.py --live --input "Unihack_ Sample Dataset - Input.csv"
  EXPECT: live upload verified: 1000 rows
  EVIDENCE: [PASS] live upload verified: 1000 rows | JUDGE_WALK_STATUS: VERIFIED + live cockpit

- [x] G9: Fresh-agent reproduction instructions match the commands and artifacts in this repository.
  EVIDENCE: docs/00-START_HERE.md lists verify_everything, judge_walk --live, official evaluator upload, verify_receipt, build_decision_log --replay, and test_receipt commands; each executable command passed in this run.

<!-- Every checked gate needs evidence. If a gate is impossible, add ABANDON: G<n> <reason>. -->
