"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
noise_prediction_loss = _module.noise_prediction_loss
predict_x0 = _module.predict_x0
AB = np.array([0.9, 0.5, 0.1])


def test_1_loss_hand_computed():
    assert np.isclose(noise_prediction_loss(np.array([1.0, 2.0]), np.array([0.0, 4.0])), (1 + 4) / 2)


def test_2_perfect_prediction_has_zero_loss():
    e = np.random.RandomState(0).randn(5, 5)
    assert noise_prediction_loss(e, e) == 0.0


def test_3_predicting_zero_costs_about_the_noise_variance():
    e = np.random.RandomState(1).randn(100000)
    assert abs(noise_prediction_loss(np.zeros_like(e), e) - 1.0) < 0.02


def test_4_true_noise_recovers_the_clean_image_exactly():
    rng = np.random.RandomState(2)
    x0, eps = rng.randn(4, 4), rng.randn(4, 4)
    for t in range(3):
        xt = np.sqrt(AB[t]) * x0 + np.sqrt(1 - AB[t]) * eps
        assert np.allclose(predict_x0(xt, eps, t, AB), x0)


def test_5_hand_computed_prediction():
    out = predict_x0(np.array([5.0]), np.array([1.0]), 1, AB)
    assert np.allclose(out, [(5.0 - np.sqrt(0.5)) / np.sqrt(0.5)])


def test_6_wrong_noise_gives_wrong_image_proportional_to_the_error():
    rng = np.random.RandomState(3)
    x0, eps = rng.randn(6), rng.randn(6)
    xt = np.sqrt(AB[1]) * x0 + np.sqrt(1 - AB[1]) * eps
    err = predict_x0(xt, eps + 0.1, 1, AB) - x0
    assert np.allclose(err, -np.sqrt(1 - AB[1]) / np.sqrt(AB[1]) * 0.1)


def test_7_inputs_untouched():
    xt, e = np.random.RandomState(4).randn(3), np.random.RandomState(5).randn(3)
    s1, s2 = xt.copy(), e.copy()
    predict_x0(xt, e, 0, AB)
    noise_prediction_loss(xt, e)
    assert np.array_equal(xt, s1) and np.array_equal(e, s2)
