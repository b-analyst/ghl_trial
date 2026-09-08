"""Did an arm actually produce episodes? Exit 0 if yes, 1 if not.

    python tools/check_arm.py logs/repair/x-ai_grok-4_3 [expected]

WHY THIS EXISTS. `inspect eval` can exit 0 having completed nothing. A provider
that rejects the request schema produces:

    ModelGenerateError: ... Invalid schema for function 'text_editor'
    Task interrupted (no samples completed before interruption)

and then returns 0. The runners checked the exit code, printed "done", and
moved on -- so a dead arm was recorded as a finished one, and the "logs already
present, delete to rerun" guard would then skip it on every later attempt while
the report read a log holding zero samples.

Checking the exit code is not checking the work. This reads the log.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python tools/check_arm.py <log-dir> [expected-episodes]")
        return 2
    d = Path(sys.argv[1])
    expected = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    logs = sorted(glob.glob(str(d / "**" / "*.eval"), recursive=True))
    if not logs:
        print(f"  NO LOG    {d.name}: the arm wrote no .eval file at all")
        return 1

    from inspect_ai.log import read_eval_log

    completed = errored = 0
    for f in logs:
        try:
            log = read_eval_log(f)
        except Exception as exc:
            print(f"  UNREADABLE {Path(f).name}: {type(exc).__name__}: {exc}")
            return 1
        for s in (log.samples or []):
            if s.error:
                errored += 1
            else:
                completed += 1

    if completed == 0:
        print(f"  EMPTY     {d.name}: {len(logs)} log(s), 0 completed episodes"
              f"{f', {errored} errored' if errored else ''}")
        return 1

    note = f", {errored} errored" if errored else ""
    if expected and completed < expected:
        print(f"  SHORT     {d.name}: {completed}/{expected} episodes{note}")
        return 1
    print(f"  ok        {d.name}: {completed} episode(s){note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
