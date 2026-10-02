def is_valid_pmf(probabilities):
    return all(p >= 0 for p in probabilities) and abs(sum(probabilities) - 1.0) < 1e-9


def expected_value_discrete(outcomes, probabilities):
    return sum(o * p for o, p in zip(outcomes, probabilities))
