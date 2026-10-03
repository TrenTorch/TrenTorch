def success_after_retries(p: float, n: int) -> float:
    """Probability that at least one of n independent attempts succeeds."""
    # TODO
    pass


def expected_attempt_cost(p: float, cost: float, n: int) -> float:
    """Expected total cost of up to n sequential attempts (later attempts only happen after failures)."""
    # TODO
    pass


def select_plan(plans: list[dict], cost_weight: float) -> int:
    """Index of the plan with the highest expected utility."""
    # TODO
    pass
