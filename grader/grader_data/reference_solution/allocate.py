"""Integer allocation helpers for settlement reconciliation."""


def allocate(total_cents: int, weights: list[int]) -> list[int]:
    """Split a total into whole-cent parts proportional to weights.

    Largest remainder: floor every share, then hand the leftover units to the
    largest remainders, ties broken by position. Parts always sum to the total.
    """
    denom = sum(weights)
    parts = [total_cents * w // denom for w in weights]
    leftover = total_cents - sum(parts)
    order = sorted(range(len(weights)),
                   key=lambda i: (-((total_cents * weights[i]) % denom), i))
    for i in order[:leftover]:
        parts[i] += 1
    return parts
