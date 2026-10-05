class CircuitBreaker:
    """closed -> open after consecutive failures -> half_open after cooldown -> closed on success."""

    def __init__(self, failure_threshold: int, cooldown: float):
        # TODO
        pass

    def allow(self, now: float) -> bool:
        """May a call be attempted at time `now`?"""
        # TODO
        pass

    def record_success(self, now: float) -> None:
        # TODO
        pass

    def record_failure(self, now: float) -> None:
        # TODO
        pass
