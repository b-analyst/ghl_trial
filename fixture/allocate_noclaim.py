"""Integer allocation helpers for settlement reconciliation."""


def allocate(total_cents: int, weights: list[int]) -> list[int]:
    """Split a total into whole-cent parts proportional to weights.

    Floors each share, so parts may sum to less than the total.
    """
    denom = sum(weights)
    return [total_cents * w // denom for w in weights]
