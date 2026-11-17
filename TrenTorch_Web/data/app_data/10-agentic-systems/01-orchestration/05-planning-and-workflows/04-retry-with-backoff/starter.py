import random


def backoff_delays(n_retries: int, base: float, factor: float, cap: float, rng: random.Random | None = None) -> list[float]:
    """Capped exponential delays, with full jitter when an rng is supplied."""
    # TODO
    pass


def total_wait(delays: list[float]) -> float:
    """Sum of the delays."""
    # TODO
    pass
