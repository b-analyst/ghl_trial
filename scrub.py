"""Scan eval logs for API keys before committing them.

    python scrub.py logs/all
    python scrub.py logs/all/x-ai_grok-4_3/<file>.eval

A .eval file records model configuration. A key that reaches one reaches the
repository's history. Exits 1 on a finding, 2 if any log could not be read --
"could not read" is a gap, not a clean bill.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Broad on purpose: a false positive costs a glance, a false negative costs a
# rotated key and a rewritten history.
PATTERNS = [
    ("OpenRouter",   re.compile(rb"sk-or-[A-Za-z0-9_\-]{12,}")),
    ("Anthropic",    re.compile(rb"sk-ant-[A-Za-z0-9_\-]{12,}")),
    ("OpenAI",       re.compile(rb"\bsk-[A-Za-z0-9]{20,}")),
    ("Google",       re.compile(rb"\bAIza[A-Za-z0-9_\-]{30,}")),
    ("bearer token", re.compile(rb"[Bb]earer\s+[A-Za-z0-9._\-]{20,}")),
    ("API_KEY=",     re.compile(rb"[A-Z_]*API_KEY[\"']?\s*[:=]\s*[\"'][^\"']{8,}")),
]


def scan(path: Path) -> tuple[list[str], str | None]:
    """(findings, error). Reads through Inspect so zstd-compressed entries are
    seen; a raw zip walk cannot decompress them."""
    try:
        from inspect_ai.log import read_eval_log
        blob = read_eval_log(str(path)).model_dump_json().encode("utf-8", "replace")
    except Exception as exc:
        return [], f"{path.name}: {exc}"
    found = [f"{label} in {path.name}: {m.group(0)[:12].decode('utf-8', 'replace')}..."
             for label, pat in PATTERNS for m in pat.finditer(blob)]
    return found, None


def main() -> int:
    targets = [Path(a) for a in sys.argv[1:]] or [Path("logs")]
    missing = [t for t in targets if not t.exists()]
    if missing:
        print("not found:", ", ".join(map(str, missing)))
        return 2
    files = [f for t in targets for f in ([t] if t.is_file() else sorted(t.rglob("*.eval")))]
    if not files:
        print("no .eval files")
        return 0

    findings, errors = [], []
    for f in files:
        found, err = scan(f)
        findings += found
        if err:
            errors.append(err)
        print(f"  {'FINDING' if found else 'unread' if err else 'clean':<8} {f}")

    print(f"\n{len(files)} log(s) scanned")
    if findings:
        print(f"\n{len(findings)} finding(s) -- do not commit. Rotate the key if it is real;")
        print("removing the line does not remove it from history once committed.")
        for x in findings[:40]:
            print(" ", x)
        return 1
    if errors:
        print(f"\n{len(errors)} log(s) could not be read -- inconclusive, not clean:")
        for e in errors[:10]:
            print(" ", e)
        return 2
    print("no known key shapes found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
