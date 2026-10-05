"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

ambiguity_decomposition = load_solution(__file__).ambiguity_decomposition


def test_hand_example():
    # Two models at 1 and 3, truth 2: the average is exactly right.
    e, ebar, a = ambiguity_decomposition(np.array([[1.0], [3.0]]), np.array([2.0]))
    assert np.isclose(e, 0.0)
    assert np.isclose(ebar, 1.0)
    assert np.isclose(a, 1.0)


def test_identity_holds_on_random_data():
    rng = np.random.default_rng(0)
    for n_models in (2, 5, 9):
        preds = rng.normal(size=(n_models, 40))
        y = rng.normal(size=40)
        e, ebar, a = ambiguity_decomposition(preds, y)
        assert np.isclose(e, ebar - a)


def test_identical_models_have_zero_ambiguity():
    preds = np.tile(np.array([1.0, 2.0, 3.0]), (4, 1))
    y = np.array([1.5, 2.5, 2.0])
    e, ebar, a = ambiguity_decomposition(preds, y)
    assert np.isclose(a, 0.0)
    assert np.isclose(e, ebar)


def test_ensemble_never_worse_than_average_member():
    rng = np.random.default_rng(2)
    preds = rng.normal(size=(6, 30))
    y = rng.normal(size=30)
    e, ebar, _ = ambiguity_decomposition(preds, y)
    assert e <= ebar + 1e-12


def test_ambiguity_is_non_negative():
    rng = np.random.default_rng(3)
    _, _, a = ambiguity_decomposition(rng.normal(size=(4, 10)), rng.normal(size=10))
    assert a >= 0.0


def test_returns_python_floats():
    result = ambiguity_decomposition(np.array([[1.0], [2.0]]), np.array([1.0]))
    assert all(isinstance(v, float) for v in result)
