import json
import re
from pathlib import Path

def mine():
    keywords = [
        'eval', 'benchmark', 'receipt', 'ledger', 'provenance', 'audit', 'lineage', 
        'replay', 'deterministic', 'diff', 'explorer', 'inspector', 'cockpit', 'graph',
        'validation', 'grounding', 'trace', 'observability', 'falsifiable', 'pipeline'
    ]

    results = []
    jsonl_path = Path('artifacts/githubawesome/transcripts.jsonl')
    if not jsonl_path.exists():
        print("transcripts.jsonl not found!")
        return

    patterns = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            vid = item['video_id']
            txt = item['transcript']
            wc = item['word_count']
            
            # Split text by periods to find distinct project pitches
            sentences = [s.strip() for s in txt.split('.') if s.strip()]
            for s in sentences:
                s_lower = s.lower()
                for kw in ['receipt', 'audit trail', 'provenance', 'clean room', 'evaluator', 'replay', 'deterministic', 'ledger', 'grounding', 'lineage', 'falsifiable']:
                    if kw in s_lower:
                        patterns.append((kw, vid, s))

    print(f"Total pattern hits found: {len(patterns)}")
    by_kw = {}
    for kw, vid, s in patterns:
        by_kw.setdefault(kw, []).append((vid, s))

    for kw, hits in by_kw.items():
        print(f"\n==================== KEYWORD: {kw.upper()} ({len(hits)} hits) ====================")
        for vid, s in hits[:4]:
            print(f"[{vid}] {s}")

if __name__ == '__main__':
    mine()

if __name__ == '__main__':
    mine()
