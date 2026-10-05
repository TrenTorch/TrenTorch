def is_statistically_significant(p_value: float, alpha: float = 0.05) -> bool:
    """
    A result is conventionally called "statistically significant" if
    its p-value falls below a chosen threshold, alpha (0.05 by far the
    most common convention).
    """
    pass


def expected_false_positives(num_tests: int, alpha: float = 0.05) -> float:
    """
    If `num_tests` independent hypothesis tests are run and EVERY
    single null hypothesis is actually true (there's no real effect
    anywhere), how many would you expect to falsely come back
    "significant" purely by chance, at threshold alpha?

    See Theory for why this number matters more than it might seem.
    """
    pass


def bonferroni_corrected_alpha(num_tests: int, alpha: float = 0.05) -> float:
    """
    The (simplest, most conservative) correction for running multiple
    tests: instead of using `alpha` for every individual test, use a
    stricter, divided threshold, so the OVERALL false-positive rate
    across all tests combined stays controlled at roughly `alpha`.
    """
    pass
