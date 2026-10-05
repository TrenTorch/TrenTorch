"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

cohens_kappa = load_solution(__file__).cohens_kappa


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_perfect_agreement_gives_one():
    y = np.array([0, 1, 2, 1, 0])
    assert np.isclose(cohens_kappa(y, y), 1.0)


def test_agreement_at_chance_level_gives_zero():
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 0, 1])
    # p_o = 0.5 and p_e = 0.5
    assert np.isclose(cohens_kappa(y_true, y_pred), 0.0)


def test_worked_example_with_eight_items():
    y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    y_pred = np.array([0, 0, 0, 1, 1, 1, 1, 0])
    # p_o = 6/8 = 0.75, p_e = 0.5, kappa = 0.25 / 0.5
    assert np.isclose(cohens_kappa(y_true, y_pred), 0.5)


def test_kappa_is_symmetric():
    rng = np.random.default_rng(6)
    a = rng.integers(0, 3, size=40)
    b = rng.integers(0, 3, size=40)
    assert np.isclose(cohens_kappa(a, b), cohens_kappa(b, a))


def test_kappa_is_invariant_to_renaming_labels():
    a = np.array([0, 0, 1, 2, 2, 1])
    b = np.array([0, 1, 1, 2, 0, 1])
    renamed_a = np.array([10, 10, 20, 30, 30, 20])
    renamed_b = np.array([10, 20, 20, 30, 10, 20])
    assert np.isclose(cohens_kappa(a, b), cohens_kappa(renamed_a, renamed_b))


def test_result_is_at_most_one():
    rng = np.random.default_rng(7)
    for _ in range(5):
        a = rng.integers(0, 4, size=25)
        b = rng.integers(0, 4, size=25)
        assert cohens_kappa(a, b) <= 1.0 + 1e-12


def test_systematic_disagreement_is_negative():
    y_true = np.array([0, 0, 0, 1, 1, 1])
    y_pred = np.array([1, 1, 1, 0, 0, 0])
    assert cohens_kappa(y_true, y_pred) < 0.0


def test_both_constant_and_identical_gives_one():
    y = np.array([3, 3, 3])
    assert cohens_kappa(y, y) == 1.0


def test_plain_accuracy_would_overstate_agreement_here():
    y_true = np.array([0] * 9 + [1])
    y_pred = np.array([0] * 9 + [0])
    # accuracy is 0.9, but kappa is 0 because the single label carries no information
    assert cohens_kappa(y_true, y_pred) == 0.0


def test_multiclass_three_way_example():
    y_true = np.array([0, 1, 2, 0, 1, 2])
    y_pred = np.array([0, 1, 2, 0, 2, 1])
    # p_o = 4/6, each class marginal is 1/3 on both sides so p_e = 1/3
    assert np.isclose(cohens_kappa(y_true, y_pred), (4 / 6 - 1 / 3) / (1 - 1 / 3))


def test_length_mismatch_raises():
    assert _raises_value_error(cohens_kappa, np.array([0, 1]), np.array([0]))


def test_empty_input_raises():
    assert _raises_value_error(cohens_kappa, np.array([]), np.array([]))


def test_does_not_modify_inputs():
    a = np.array([0, 1, 1])
    b = np.array([0, 0, 1])
    before_a, before_b = a.copy(), b.copy()
    cohens_kappa(a, b)
    assert np.array_equal(a, before_a)
    assert np.array_equal(b, before_b)
