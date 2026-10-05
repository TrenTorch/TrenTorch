import json


def step_efficiency(n_steps: int, n_optimal: int, succeeded: bool) -> float:
    """0.0 on failure, else min(1, n_optimal / n_steps)."""
    # TODO
    pass


def redundancy_rate(actions: list[tuple[str, dict]]) -> float:
    """Fraction of actions that repeat an earlier action exactly."""
    # TODO
    pass
