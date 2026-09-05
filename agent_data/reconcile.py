"""Daily settlement reconciliation report.

Downstream ledger import parses this output. The column totals are matched
against the bank file, so the numbers here are contractual.
"""

from allocate import allocate

# Three-way desk split, unchanged since the 2019 ledger migration.
DESKS = ["emea", "amer", "apac"]


def daily_report(total_cents: int) -> dict[str, int]:
    parts = allocate(total_cents, [1, 1, 1])
    return dict(zip(DESKS, parts))


if __name__ == "__main__":
    print(daily_report(100))
