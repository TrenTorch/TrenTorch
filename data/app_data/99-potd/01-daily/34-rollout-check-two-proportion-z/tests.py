"""
pytest data/app_data/99-potd/01-daily/34-rollout-check-two-proportion-z/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
two_proportion_z_test = _module.two_proportion_z_test

TOLERANCE = 1e-4


def test_example_matches_the_specs_worked_value():
    p1, p2, z, pvalue = two_proportion_z_test(5000, 250, 5000, 300)
    assert abs(p1 - 0.05) < TOLERANCE
    assert abs(p2 - 0.06) < TOLERANCE
    assert abs(z - 2.193172) < TOLERANCE
    assert abs(pvalue - 0.028295) < TOLERANCE


def test_zero_successes_in_both_groups_collapses_to_no_evidence():
    p1, p2, z, pvalue = two_proportion_z_test(1000, 0, 1000, 0)
    assert p1 == 0.0
    assert p2 == 0.0
    assert z == 0.0
    assert abs(pvalue - 1.0) < 1e-9


def test_identical_conversion_rates_give_z_zero_pvalue_one():
    p1, p2, z, pvalue = two_proportion_z_test(2000, 100, 3000, 150)
    assert abs(p1 - p2) < 1e-12
    assert abs(z) < 1e-9
    assert abs(pvalue - 1.0) < 1e-6


def test_larger_treatment_rate_gives_a_positive_z():
    p1, p2, z, pvalue = two_proportion_z_test(1000, 50, 1000, 100)
    assert z > 0
    assert 0 <= pvalue <= 1


def test_smaller_treatment_rate_gives_a_negative_z():
    p1, p2, z, pvalue = two_proportion_z_test(1000, 100, 1000, 50)
    assert z < 0
    assert 0 <= pvalue <= 1


def test_pooled_proportion_is_used_not_the_simple_average():
    # With very different n's, pooled p differs sharply from (p1+p2)/2.
    p1, p2, z, pvalue = two_proportion_z_test(10, 5, 10_000_000, 5_000_000)
    # p1 = p2 = 0.5 exactly, so regardless of pooling method z must be 0.
    assert abs(p1 - 0.5) < TOLERANCE
    assert abs(p2 - 0.5) < TOLERANCE
    assert abs(z) < 1e-6
