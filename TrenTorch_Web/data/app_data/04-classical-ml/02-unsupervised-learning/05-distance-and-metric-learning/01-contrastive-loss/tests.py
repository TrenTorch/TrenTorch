"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
contrastive_loss = _module.contrastive_loss


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_similar_pair_loss_is_squared_distance():
    assert np.isclose(contrastive_loss(np.array([2.0]), np.array([1]))[0], 4.0)


def test_similar_pair_at_zero_distance_has_zero_loss():
    assert contrastive_loss(np.array([0.0]), np.array([1]))[0] == 0.0


def test_dissimilar_pair_beyond_margin_has_zero_loss():
    assert contrastive_loss(np.array([2.0]), np.array([0]), margin=1.0)[0] == 0.0


def test_dissimilar_pair_exactly_at_margin_has_zero_loss():
    assert contrastive_loss(np.array([1.0]), np.array([0]), margin=1.0)[0] == 0.0


def test_dissimilar_pair_inside_margin_is_penalized_by_gap_squared():
    assert np.isclose(contrastive_loss(np.array([0.25]), np.array([0]), margin=1.0)[0], 0.5625)


def test_dissimilar_pair_at_zero_distance_costs_margin_squared():
    assert np.isclose(contrastive_loss(np.array([0.0]), np.array([0]), margin=2.0)[0], 4.0)


def test_loss_keeps_the_input_shape():
    d = np.zeros((2, 3))
    s = np.ones((2, 3))
    assert contrastive_loss(d, s).shape == (2, 3)


def test_batch_mean_matches_hand_computation():
    d = np.array([0.5, 2.0, 0.25])
    s = np.array([1, 0, 0])
    per_pair = contrastive_loss(d, s, margin=1.0)
    # 0.25 (similar), 0 (dissimilar and far), 0.5625 (dissimilar and close)
    assert np.isclose(per_pair.mean(), (0.25 + 0.0 + 0.5625) / 3)


def test_loss_is_never_negative():
    rng = np.random.default_rng(0)
    d = rng.uniform(0, 3, size=50)
    s = rng.integers(0, 2, size=50)
    assert np.all(contrastive_loss(d, s, margin=1.5) >= 0.0)


def test_dissimilar_loss_is_continuous_at_the_margin():
    just_inside = contrastive_loss(np.array([1.0 - 1e-9]), np.array([0]), margin=1.0)[0]
    assert just_inside < 1e-15


def test_negative_distance_raises():
    assert _raises_value_error(contrastive_loss, np.array([-0.1]), np.array([1]))


def test_negative_margin_raises():
    assert _raises_value_error(contrastive_loss, np.array([0.5]), np.array([0]), -1.0)


def test_non_binary_similarity_flag_raises():
    assert _raises_value_error(contrastive_loss, np.array([0.5]), np.array([0.5]))


def test_shape_mismatch_raises():
    assert _raises_value_error(contrastive_loss, np.array([0.5, 1.0]), np.array([1]))


def test_inputs_are_not_modified():
    d = np.array([0.5, 2.0])
    s = np.array([1, 0])
    d0, s0 = d.copy(), s.copy()
    contrastive_loss(d, s)
    assert np.array_equal(d, d0) and np.array_equal(s, s0)
