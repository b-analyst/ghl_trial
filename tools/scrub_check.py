"""Scan eval logs for credentials before they are committed.

    python tools/scrub_check.py logs/all
    python tools/scrub_check.py logs/all/qwen_qwen3_8-27b/<file>.eval

Exits non-zero if anything resembling an API key is found. Run it before
committing any log produced with a paid key: a .eval file is a zip archive of
JSON, it records model configuration, and a key that reaches it reaches the
repository's history permanently.

Nothing found is not a guarantee -- this matches known key shapes, not every
possible secret. It is a cheap check, not an audit.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

# Known key shapes. Deliberately broad: a false positive costs a glance, a
# false negative costs a rotated key and a rewritten history.
PATTERNS = [
    ("OpenRouter",  re.compile(rb"sk-or-[A-Za-z0-9_\-]{12,}")),
    ("Anthropic",   re.compile(rb"sk-ant-[A-Za-z0-9_\-]{12,}")),
    ("OpenAI",      re.compile(rb"\bsk-[A-Za-z0-9]{20,}")),
    ("Google",      re.compile(rb"\bAIza[A-Za-z0-9_\-]{30,}")),
    ("bearer token", re.compile(rb"[Bb]earer\s+[A-Za-z0-9._\-]{20,}")),
    ("env var name", re.compile(rb"[A-Z_]*API_KEY[\"']?\s*[:=]\s*[\"'][^\"']{8,}")),
]


def scan_bytes(blob: bytes, where: str) -> list[str]:
    out = []
    for label, pat in PATTERNS:
        for m in pat.finditer(blob):
            snippet = m.group(0)[:12].decode("utf-8", "replace")
            out.append(f"{label} in {where}: {snippet}...")
    return out


def scan_file(path: Path) -> tuple[list[str], list[str]]:
    """Return (findings, unscannable). These are NOT the same thing.

    An .eval is a zip whose entries Inspect may compress with zstd, which
    Python's stdlib zipfile cannot decompress. An earlier version of this
    script counted every such entry as a finding and reported 252 "leaks"
    across the pilot logs, all of them decompression errors. Reading the log
    through Inspect's own reader avoids the problem entirely; the zip path
    remains only as a fallback for non-.eval inputs.
    """
    findings: list[str] = []
    unscannable: list[str] = []

    if path.suffix == ".eval":
        try:
            from inspect_ai.log import read_eval_log
            log = read_eval_log(str(path))
            # Serialise the whole log -- header, config, model args, every
            # message and tool call -- and scan the text.
            blob = log.model_dump_json().encode("utf-8", "replace")
            return scan_bytes(blob, path.name), []
        except Exception as exc:
            unscannable.append(f"{path.name}: could not read via inspect_ai ({exc})")

    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                try:
                    findings += scan_bytes(z.read(name), f"{path.name}::{name}")
                except Exception as exc:
                    unscannable.append(f"{path.name}::{name}: {exc}")
    else:
        try:
            findings += scan_bytes(path.read_bytes(), path.name)
        except Exception as exc:
            unscannable.append(f"{path.name}: {exc}")

    return findings, unscannable


def main() -> int:
    # Every argument, not just the first. This read sys.argv[1] alone and
    # ignored the rest in silence, so `scrub_check.py logs/a logs/b logs/c`
    # scanned logs/a and then printed "Safe to commit" -- a key-leak guard
    # reporting clean on a third of what it was asked to check. Anything that
    # answers "is it safe to commit" has to fail loudly or not at all.
    targets = [Path(a) for a in sys.argv[1:]] or [Path("logs")]

    missing = [t for t in targets if not t.exists()]
    if missing:
        for t in missing:
            print(f"not found: {t}")
        return 2

    files: list[Path] = []
    for t in targets:
        found = [t] if t.is_file() else sorted(t.rglob("*.eval"))
        if not found:
            print(f"no .eval files under {t}")
        files += found
    if not files:
        return 0
    if len(targets) > 1:
        print(f"scanning {len(files)} log(s) across {len(targets)} paths: "
              + ", ".join(str(t) for t in targets))
        print()

    all_findings: list[str] = []
    all_unscannable: list[str] = []
    for f in files:
        found, unread = scan_file(f)
        if found:
            status = f"{len(found)} FINDING(S)"
        elif unread:
            status = "UNSCANNABLE"
        else:
            status = "clean"
        print(f"  {status:<16} {f}")
        all_findings += found
        all_unscannable += unread

    print(f"\n{len(files)} log(s) scanned.")

    if all_unscannable:
        print(f"\n{len(all_unscannable)} entr(ies) could not be read. NOT findings --")
        print("this check could not see inside them, which is a gap, not a leak:")
        for u in all_unscannable[:10]:
            print(f"  {u}")
        if len(all_unscannable) > 10:
            print(f"  ... and {len(all_unscannable) - 10} more")

    if all_findings:
        print(f"\n{len(all_findings)} finding(s) -- DO NOT COMMIT:")
        for f in all_findings[:40]:
            print(f"  {f}")
        print("\nRotate the key if it is real. Removing the line from a file does")
        print("not remove it from git history once committed.")
        return 1

    if all_unscannable:
        print("\nNo key shapes found in what could be read, but coverage was")
        print("incomplete. Treat this as inconclusive rather than clean.")
        return 2

    print("\nNo known key shapes found. Safe to commit as far as this check sees.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
