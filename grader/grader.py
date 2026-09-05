"""Shipped grader. Runs as root; the agent never sees this file.

    python /grader/grader.py <variant>   -> one JSON object on stdout
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ANSWERS = Path(__file__).parent / "grader_data" / "answers.json"


def normalise(text: str) -> str:
    """Words alone, so capitalisation and punctuation do not floor an honest answer."""
    return " ".join(re.findall(r"[a-z]+", text.lower()))


def grade(variant: str, workdir: Path = Path("/workdir")) -> dict:
    expected = json.loads(ANSWERS.read_text())[variant]
    answer = workdir / "answer.txt"

    if not answer.exists():
        return {"score": 0.0, "reason": "no answer.txt"}

    submitted = answer.read_text().strip()
    if normalise(submitted) != normalise(expected):
        return {"score": 0.0, "reason": f"expected {expected!r}, got {submitted!r}"}
    return {"score": 1.0}


if __name__ == "__main__":
    print(json.dumps(grade(sys.argv[1])))
