def success_after_retries(p, n):
    return 1.0 - (1.0 - p) ** n


def expected_attempt_cost(p, cost, n):
    return float(cost * sum((1.0 - p) ** k for k in range(n)))


def select_plan(plans, cost_weight):
    def utility(pl):
        return pl["value"] * success_after_retries(pl["p"], pl["attempts"]) - cost_weight * expected_attempt_cost(pl["p"], pl["cost"], pl["attempts"])
    utils = [utility(pl) for pl in plans]
    return utils.index(max(utils))
