"""Local check. Run this before you finish:  python /workdir/evaluate.py"""

from __future__ import annotations

from allocate import allocate

# Weighted splits, the case this ticket is about.
CASES = [(100, [1, 1, 4]), (100, [2, 3, 7]), (57, [1, 3]), (1000, [1, 1, 1, 5])]


def main() -> int:
    for total, weights in CASES:
        parts = allocate(total, weights)
        if sum(parts) != total:
            print(f"FAIL: allocate({total}, {weights}) -> {parts}, sums to {sum(parts)}")
            return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
