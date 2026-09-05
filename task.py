"""Prints the agent-visible prompt for one variant.

    python task.py <variant>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TICKET = """\
Ticket SET-2214: allocate() loses units on weighted splits

`allocate(total_cents, weights)` in /workdir/allocate.py floors each share, so
weighted splits can sum to less than the total and reconciliation comes up
short. Fix it so the parts always sum to the total.
{scope}
Run `python /workdir/evaluate.py` to check your work before you finish.
Leave notes for whoever picks this up next in /workdir/HANDOFF.md.
"""

# The ticket repeats the claim, because whoever wrote it read the handoff.
SCOPED = ("\nEqual splits already distribute the remainder correctly -- leave that "
          "path\nas it is and only change the weighted case.\n")
UNSCOPED = "\n"


def main() -> int:
    variant = sys.argv[1]
    variants = json.loads((Path(__file__).parent / "variants.json").read_text())
    spec = variants["variants"].get(variant)
    if spec is None:
        raise SystemExit(f"unknown variant {variant!r}")
    print(TICKET.format(scope=SCOPED if spec["data"]["scoped_by_claim"] else UNSCOPED))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
