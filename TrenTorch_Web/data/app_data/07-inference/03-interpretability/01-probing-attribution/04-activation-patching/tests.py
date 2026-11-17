"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
patch_rows = _module.patch_rows
recovery = _module.recovery
patching_scan = _module.patching_scan


def test_1_patch_rows_hand_computed():
    clean = np.arange(6.0).reshape(3, 2)
    corrupt = np.zeros((3, 2))
    out = patch_rows(clean, corrupt, [0, 2])
    assert np.allclose(out, [[0, 1], [0, 0], [4, 5]])


def test_2_recovery_endpoints():
    assert np.isclose(recovery(5.0, 1.0, 1.0), 0.0)
    assert np.isclose(recovery(5.0, 1.0, 5.0), 1.0)
    assert np.isclose(recovery(5.0, 1.0, 3.0), 0.5)


def test_3_recovery_can_exceed_one_or_go_negative():
    assert recovery(2.0, 0.0, 3.0) > 1.0
    assert recovery(2.0, 0.0, -1.0) < 0.0


def test_4_scan_finds_the_one_position_that_matters():
    w = np.array([[0.0, 0.0], [3.0, 1.0], [0.0, 0.0]])
    model = lambda acts: float((acts * w).sum())
    rng = np.random.RandomState(0)
    clean, corrupt = rng.randn(3, 2), rng.randn(3, 2)
    out = patching_scan(model, clean, corrupt)
    assert np.allclose(out, [0.0, 1.0, 0.0])


def test_5_linear_model_recoveries_sum_to_one():
    rng = np.random.RandomState(1)
    w = rng.randn(5, 4)
    model = lambda acts: float((acts * w).sum())
    clean, corrupt = rng.randn(5, 4), rng.randn(5, 4)
    assert np.isclose(patching_scan(model, clean, corrupt).sum(), 1.0)


def test_6_nonlinear_model_matches_explicit_loop():
    rng = np.random.RandomState(2)
    clean, corrupt = rng.randn(4, 3), rng.randn(4, 3)
    model = lambda acts: float(np.tanh(acts.sum(axis=1)).prod())
    out = patching_scan(model, clean, corrupt)
    for t in range(4):
        patched = corrupt.copy()
        patched[t] = clean[t]
        expected = (model(patched) - model(corrupt)) / (model(clean) - model(corrupt))
        assert np.isclose(out[t], expected)


def test_7_inputs_are_not_modified():
    rng = np.random.RandomState(3)
    clean, corrupt = rng.randn(3, 2), rng.randn(3, 2)
    s1, s2 = clean.copy(), corrupt.copy()
    patching_scan(lambda a: float(a.sum()), clean, corrupt)
    patch_rows(clean, corrupt, [1])
    assert np.array_equal(clean, s1) and np.array_equal(corrupt, s2)
