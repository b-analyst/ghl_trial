"""Integer allocation helpers for settlement reconciliation."""


def allocate(total_cents: int, weights: list[int]) -> list[int]:
    """Split a total into whole-cent parts proportional to weights.

    Equal splits distribute the remainder to the first part; weighted splits
    floor each share and may lose units.
    """
    denom = sum(weights)
    return [total_cents * w // denom for w in weights]
