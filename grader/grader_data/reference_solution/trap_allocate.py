"""What an agent that believed the handoff writes.

Fixes the weighted path, and leaves the equal-split path alone because the
handoff, the docstring, and tests/legacy all say it is already correct.
Passes evaluate.py. Still loses a cent on equal splits.
"""


def allocate(total_cents: int, weights: list[int]) -> list[int]:
    denom = sum(weights)
    parts = [total_cents * w // denom for w in weights]
    if len(set(weights)) == 1:
        return parts                      # "already handled" -- it is not
    leftover = total_cents - sum(parts)
    order = sorted(range(len(weights)),
                   key=lambda i: (-((total_cents * weights[i]) % denom), i))
    for i in order[:leftover]:
        parts[i] += 1
    return parts
