import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

FREEZE_COMMIT = "38db2af"
FREEZE_TAG = "bar-4-freeze"
# Allowlisted post-freeze addition: UAT verification tooling, not pipeline code.
ALLOWLIST = {"unihack_catalog/verification_ledger.py"}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    ).stdout.strip()


def check(label: str, ok: bool, detail: str = "") -> int:
    print(f"  [PASS] {label}" if ok else f"  [FAIL] {label}")
    if detail and not ok:
        print(f"         {detail}")
    return 0 if ok else 1


def main() -> int:
    failed = 0
    print("=== FREEZE INTEGRITY CHECK ===")

    try:
        tag_commit = git("rev-list", "-n", "1", FREEZE_TAG)
        freeze_commit = git("rev-parse", f"{FREEZE_COMMIT}^{{commit}}")
        failed += check(
            f"tag {FREEZE_TAG} points at {FREEZE_COMMIT}",
            tag_commit == freeze_commit,
            f"tag resolves to {tag_commit}",
        )
    except subprocess.CalledProcessError as e:
        failed += check(f"tag {FREEZE_TAG} resolves", False, e.stderr.strip())

    try:
        diff = git("diff", "--name-only", f"{FREEZE_COMMIT}..HEAD", "--", "unihack_catalog/")
        changed = [p for p in diff.splitlines() if p]
        offenders = [p for p in changed if p not in ALLOWLIST]
        failed += check(
            "no pipeline changes since freeze (allowlisted verification_ledger.py)",
            not offenders,
            f"unexpected: {offenders}",
        )
    except subprocess.CalledProcessError as e:
        failed += check("freeze diff resolves", False, e.stderr.strip())

    try:
        worktree = git("status", "--porcelain", "--", "unihack_catalog/")
        dirty = [p.split()[-1] for p in worktree.splitlines() if p]
        offenders = [p for p in dirty if p not in ALLOWLIST]
        failed += check(
            "working tree under unihack_catalog/ untouched",
            not offenders,
            f"dirty: {offenders}",
        )
    except subprocess.CalledProcessError as e:
        failed += check("working-tree status resolves", False, e.stderr.strip())

    print("\nPost-freeze commits (must read as docs/tooling only):")
    try:
        for commit in git("log", "--format=%h %s", f"{FREEZE_COMMIT}..HEAD").splitlines():
            print(f"  {commit}")
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] {e.stderr.strip()}")

    print("\nWorking tree audit (git status --porcelain):")
    status = git("status", "--porcelain")
    print("  <clean>" if not status else "  " + status.replace("\n", "\n  "))

    print("\n" + "=" * 40)
    print("FREEZE CHECK: PASSED" if failed == 0 else "FREEZE CHECK: FAILED")
    print("=" * 40)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())