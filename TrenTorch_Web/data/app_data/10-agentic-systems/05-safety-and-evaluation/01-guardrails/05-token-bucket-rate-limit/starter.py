class TokenBucket:
    """Starts full; refills continuously at refill_rate tokens per time unit."""

    def __init__(self, capacity: float, refill_rate: float):
        # TODO
        pass

    def try_acquire(self, now: float, n: float = 1) -> bool:
        """Refill up to `now`, then take n tokens if available."""
        # TODO
        pass
