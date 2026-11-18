"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import math

pass_hat_k = _module.pass_hat_k
mean_pass_hat_k = _module.mean_pass_hat_k


def test_1_k_one_is_the_success_rate():
    assert math.isclose(pass_hat_k(10, 7, 1), 0.7)


def test_2_hand_computed():
    # C(3,2)/C(5,2) = 3/10
    assert math.isclose(pass_hat_k(5, 3, 2), 0.3)


def test_3_all_successes_is_one_and_too_few_successes_is_zero():
    assert pass_hat_k(8, 8, 5) == 1.0 and pass_hat_k(8, 2, 3) == 0.0


def test_4_decreases_as_k_grows():
    vals = [pass_hat_k(20, 15, k) for k in (1, 2, 4, 8)]
    assert vals == sorted(vals, reverse=True) and vals[-1] < 0.1


def test_5_matches_binomial_definition():
    from math import comb
    for n, c, k in [(10, 6, 3), (12, 12, 4), (30, 20, 7)]:
        assert math.isclose(pass_hat_k(n, c, k), comb(c, k) / comb(n, k))


def test_6_reliability_and_best_of_k_move_in_opposite_directions():
    # an agent that succeeds 80% of the time: pass@k rises with k, pass^k falls
    n, c = 50, 40
    pass_at = lambda k: 1.0 if n - c < k else 1 - math.prod(1 - k / i for i in range(n - c + 1, n + 1))
    assert pass_hat_k(n, c, 5) < pass_hat_k(n, c, 1)
    assert pass_at(5) > pass_at(1)


def test_7_mean_over_tasks():
    assert math.isclose(mean_pass_hat_k([4, 4], [4, 0], 2), 0.5)
