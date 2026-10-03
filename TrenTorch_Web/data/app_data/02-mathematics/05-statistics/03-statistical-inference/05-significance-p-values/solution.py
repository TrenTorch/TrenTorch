def is_statistically_significant(p_value: float, alpha: float = 0.05) -> bool:
    return p_value < alpha


def expected_false_positives(num_tests: int, alpha: float = 0.05) -> float:
    return num_tests * alpha


def bonferroni_corrected_alpha(num_tests: int, alpha: float = 0.05) -> float:
    return alpha / num_tests
