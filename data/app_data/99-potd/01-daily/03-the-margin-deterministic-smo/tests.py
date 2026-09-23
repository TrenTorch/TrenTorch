"""
pytest data/app_data/03-classical-ml/04-support-vector-machines/04-the-margin-deterministic-smo/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
smo_fit = _module.smo_fit
svm_decision_function = _module.svm_decision_function


def test_example_one_matches_the_specs_worked_derivation():
    X = np.array([[2.0, 2.0], [3.0, 3.0], [0.0, 0.0], [1.0, 0.0]])
    y = np.array([1.0, 1.0, -1.0, -1.0])
    alpha, b = smo_fit(X, y, C=1.0, tol=0.001, max_passes=10)
    assert np.allclose(alpha, [0.4, 0.0, 0.0, 0.4], atol=1e-4)
    assert np.isclose(b, -1.4, atol=1e-4)
    queries = np.array([[2.0, 0.0], [0.5, 2.0]])
    scores = svm_decision_function(X, y, alpha, b, queries)
    assert np.allclose(scores, [-0.6, 0.4], atol=1e-4)


def test_example_two_shows_the_box_constraint_binding():
    # Same data as Example 1, but C=0.25 is small enough to clip both
    # support vectors below the earlier unconstrained optimum of 0.4.
    X = np.array([[2.0, 2.0], [3.0, 3.0], [0.0, 0.0], [1.0, 0.0]])
    y = np.array([1.0, 1.0, -1.0, -1.0])
    alpha, b = smo_fit(X, y, C=0.25, tol=0.001, max_passes=5)
    assert np.allclose(alpha, [0.25, 0.0, 0.0, 0.25], atol=1e-4)
    assert np.isclose(b, -1.125, atol=1e-4)
    queries = np.array([[2.0, 0.0], [0.5, 2.0]])
    scores = svm_decision_function(X, y, alpha, b, queries)
    assert np.allclose(scores, [-0.625, 0.0], atol=1e-4)


def test_tol_too_loose_makes_smo_fit_a_total_no_op():
    # At alpha=0, b=0, E_i = -y_i, so y_i*E_i = -1 for every point,
    # regardless of X. With tol=1.0 (the constraint's own upper bound),
    # "-1 < -tol" is "-1 < -1", which is FALSE -- every point is
    # (correctly) judged to already satisfy KKT well enough, and
    # nothing should ever update.
    X = np.array([[5.0], [-5.0]])
    y = np.array([1.0, -1.0])
    alpha, b = smo_fit(X, y, C=1.0, tol=1.0, max_passes=5)
    assert np.allclose(alpha, [0.0, 0.0], atol=1e-9)
    assert np.isclose(b, 0.0, atol=1e-9)


def test_tight_tol_on_the_same_data_does_make_real_progress():
    # Same two-point dataset as the no-op test above, but a tight tol
    # lets the KKT check actually trigger -- contrasting directly with
    # the loose-tol case to catch a flipped tolerance-direction bug.
    X = np.array([[5.0], [-5.0]])
    y = np.array([1.0, -1.0])
    alpha, b = smo_fit(X, y, C=1.0, tol=0.001, max_passes=5)
    assert not np.allclose(alpha, [0.0, 0.0], atol=1e-9)


def test_all_one_label_data_can_never_leave_alpha_at_zero():
    # Every pair here shares a label, so at every step L = H = 0 (the
    # box bounds collapse to a single point whenever alpha_i = alpha_j,
    # which starts true and can never change since every pair skips).
    # This is a hard invariant, not a coincidence of one dataset: with
    # a single class present, sum(alpha_i * y_i) = 0 combined with
    # alpha_i >= 0 forces every alpha_i to stay exactly 0.
    X = np.array([[1.0], [2.0], [3.0]])
    y = np.array([1.0, 1.0, 1.0])
    alpha, b = smo_fit(X, y, C=1.0, tol=0.001, max_passes=5)
    assert np.allclose(alpha, [0.0, 0.0, 0.0], atol=1e-9)
    assert np.isclose(b, 0.0, atol=1e-9)


def test_kkt_stationarity_holds_at_the_examples_own_converged_alpha():
    # Using ONLY the alpha/b the spec itself derives for Example 1: the
    # two support vectors (0 < alpha < C) must sit exactly on the
    # margin (y*f(x) == 1), and the two zero-alpha points must sit
    # comfortably past it (y*f(x) > 1). A solver that stopped early or
    # overshot would violate this on the very data it was fit to.
    X = np.array([[2.0, 2.0], [3.0, 3.0], [0.0, 0.0], [1.0, 0.0]])
    y = np.array([1.0, 1.0, -1.0, -1.0])
    alpha = np.array([0.4, 0.0, 0.0, 0.4])
    b = -1.4
    scores = svm_decision_function(X, y, alpha, b, X)
    margins = y * scores
    assert np.isclose(margins[0], 1.0, atol=1e-6)
    assert np.isclose(margins[3], 1.0, atol=1e-6)
    assert margins[1] > 1.0
    assert margins[2] > 1.0


def test_box_constraint_is_always_respected():
    rng = np.random.default_rng(5)
    X = rng.normal(size=(12, 3))
    y = rng.choice([-1.0, 1.0], size=12)
    C = 0.3
    alpha, _ = smo_fit(X, y, C=C, tol=0.01, max_passes=10)
    assert np.all(alpha >= -1e-9)
    assert np.all(alpha <= C + 1e-9)


def test_dual_equality_constraint_holds_after_training():
    # sum(alpha_i * y_i) == 0 is preserved by construction (every
    # two-variable update moves alpha_i and alpha_j by matched amounts
    # in opposite directions), so it must still hold exactly at the end
    # regardless of how many updates happened.
    rng = np.random.default_rng(7)
    X = rng.normal(size=(10, 2))
    y = rng.choice([-1.0, 1.0], size=10)
    alpha, _ = smo_fit(X, y, C=1.0, tol=0.01, max_passes=10)
    assert abs(np.sum(alpha * y)) < 1e-6


def test_high_dimensional_few_points_stays_finite_and_well_shaped():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(6, 18))
    y = np.array([1.0, 1.0, 1.0, -1.0, -1.0, -1.0])
    alpha, b = smo_fit(X, y, C=1.0, tol=0.01, max_passes=20)
    assert alpha.shape == (6,)
    assert np.all(np.isfinite(alpha))
    assert np.isfinite(b)
    queries = rng.normal(size=(4, 18))
    scores = svm_decision_function(X, y, alpha, b, queries)
    assert scores.shape == (4,)
    assert np.all(np.isfinite(scores))


def test_live_updates_within_a_pass_are_not_a_batch_update():
    # Engineered so that using STALE (pre-pass) alpha/b instead of the
    # LIVE, mid-pass values inside the same sweep gives a detectably
    # different final answer -- verified against a deliberately
    # batched mutant offline; this asserts the correct (live) result.
    X = np.array(
        [
            [-2.079968, 1.500902],
            [1.881129, -3.902070],
            [-2.604359, 0.255681],
            [-0.632485, -0.033602],
        ]
    )
    y = np.array([1.0, 1.0, -1.0, 1.0])
    alpha, b = smo_fit(X, y, C=1.0, tol=0.01, max_passes=3)
    expected_alpha = np.array([0.05346664, 0.0, 0.54792482, 0.49445818])
    assert np.allclose(alpha, expected_alpha, atol=1e-4)
    assert np.isclose(b, 1.6318428299864243, atol=1e-4)


def test_svm_decision_function_returns_one_score_per_query():
    rng = np.random.default_rng(11)
    X = rng.normal(size=(15, 4))
    y = rng.choice([-1.0, 1.0], size=15)
    alpha, b = smo_fit(X, y, C=1.0, tol=0.01, max_passes=5)
    queries = rng.normal(size=(9, 4))
    scores = svm_decision_function(X, y, alpha, b, queries)
    assert scores.shape == (9,)


def test_decision_function_uses_the_linear_kernel_directly():
    # A minimal, hand-checkable sanity case independent of smo_fit:
    # one support vector at x=(1,0) with alpha=1, y=1, b=0, evaluated
    # at a query -- f(q) must equal the plain dot product x . q.
    X = np.array([[1.0, 0.0]])
    y = np.array([1.0])
    alpha = np.array([1.0])
    b = 0.0
    queries = np.array([[3.0, 4.0], [0.0, 5.0]])
    scores = svm_decision_function(X, y, alpha, b, queries)
    assert np.allclose(scores, [3.0, 0.0])
