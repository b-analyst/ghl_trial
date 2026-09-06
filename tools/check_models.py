"""Validate the model roster against OpenRouter's live catalogue.

    python tools/check_models.py [roster]

Reads OPENROUTER_API_KEY from the environment. Prints one line per roster entry
and exits non-zero if any id is unknown, so a retired slug fails in a second
rather than after a batch has burned tokens on 404s.

The key is read from the environment and never printed, logged, or written to
disk by this script.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = "https://openrouter.ai/api/v1/models"


def read_roster(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [s.strip() for s in lines if s.strip() and not s.lstrip().startswith("#")]


def fetch_catalogue(key: str | None) -> set[str]:
    req = urllib.request.Request(CATALOGUE, headers={"Accept": "application/json"})
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    return {m["id"] for m in payload.get("data", [])}


def main() -> int:
    roster_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "tools" / "models.txt"
    if not roster_path.exists():
        print(f"roster not found: {roster_path}")
        return 2

    roster = read_roster(roster_path)
    if not roster:
        print("roster is empty")
        return 2

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("note: OPENROUTER_API_KEY unset -- the catalogue is public, so this")
        print("      still validates ids, but it will not confirm your key works.")

    try:
        known = fetch_catalogue(key)
    except Exception as exc:
        print(f"could not reach OpenRouter: {exc}")
        print("check the id list by hand at https://openrouter.ai/models")
        return 2

    bad = 0
    for model_id in roster:
        if model_id in known:
            print(f"  ok       {model_id}")
        else:
            bad += 1
            near = sorted(m for m in known if model_id.split("/")[-1][:6] in m)[:3]
            hint = ("  did you mean: " + ", ".join(near)) if near else ""
            print(f"  UNKNOWN  {model_id}{hint}")

    print(f"\n{len(roster) - bad} of {len(roster)} ids resolve.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
