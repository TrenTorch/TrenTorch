import numpy as np
from _load import load_solution


_module = load_solution(__file__)
focal_loss = _module.focal_loss


def test_shape_mismatch():
    logits = np.array([0.0, 1.0])
    labels = np.array([0.0])
    try:
        focal_loss(logits, labels)
        assert False
    except ValueError:
        pass


def test_negative_gamma():
    logits = np.array([0.0])
    labels = np.array([0.0])
    try:
        focal_loss(logits, labels, gamma=-1.0)
        assert False
    except ValueError:
        pass


def test_perfect_prediction():
    logits = np.array([100.0, -100.0])
    labels = np.array([1.0, 0.0])
    loss = focal_loss(logits, labels, gamma=2.0)
    assert loss < 1e-3


def test_worst_prediction():
    logits = np.array([-100.0, 100.0])
    labels = np.array([1.0, 0.0])
    loss = focal_loss(logits, labels, gamma=2.0)
    assert loss > 10.0


def test_gamma_zero_is_ce():
    logits = np.array([0.5, -0.5])
    labels = np.array([1.0, 0.0])
    loss_focal = focal_loss(logits, labels, gamma=0.0)
    probs = 1.0 / (1.0 + np.exp(-logits))
    ce = -np.mean(
        labels * np.log(np.clip(probs, 1e-7, 1.0))
        + (1.0 - labels) * np.log(np.clip(1.0 - probs, 1e-7, 1.0))
    )
    np.testing.assert_allclose(loss_focal, ce, rtol=1e-5)


def test_scalar_input():
    loss = focal_loss(np.array([0.0]), np.array([1.0]))
    assert isinstance(loss, (np.ndarray, float, np.floating))


def test_batch_hard_examples():
    logits = np.array([-1.0, -1.0, 1.0, 1.0])
    labels = np.array([1.0, 1.0, 0.0, 0.0])
    loss = focal_loss(logits, labels, gamma=2.0)
    assert loss > 0.0
    assert np.isfinite(loss)


def test_batch_easy_examples():
    logits = np.array([10.0, 10.0, -10.0, -10.0])
    labels = np.array([1.0, 1.0, 0.0, 0.0])
    loss = focal_loss(logits, labels, gamma=2.0)
    assert loss < 0.01


def test_monotonic_gamma():
    logits = np.array([0.0, 0.0, 0.0])
    labels = np.array([1.0, 1.0, 1.0])
    loss_g0 = focal_loss(logits, labels, gamma=0.0)
    loss_g1 = focal_loss(logits, labels, gamma=1.0)
    loss_g2 = focal_loss(logits, labels, gamma=2.0)
    assert loss_g0 >= loss_g1 >= loss_g2


def test_uniform_labels():
    logits = np.array([0.0, 0.0, 0.0, 0.0])
    labels = np.array([1.0, 0.0, 1.0, 0.0])
    loss = focal_loss(logits, labels, gamma=2.0)
    assert loss > 0.0
    assert np.isfinite(loss)


def test_2d_input():
    logits = np.array([[0.5, -0.5], [1.0, -1.0]])
    labels = np.array([[1.0, 0.0], [1.0, 0.0]])
    loss = focal_loss(logits, labels)
    assert isinstance(loss, (np.ndarray, float, np.floating))
    assert np.isfinite(loss)


def test_all_zeros():
    logits = np.zeros(5)
    labels = np.zeros(5)
    loss = focal_loss(logits, labels, gamma=2.0)
    assert np.isfinite(loss)


def test_all_ones():
    logits = np.ones(5)
    labels = np.ones(5)
    loss = focal_loss(logits, labels, gamma=2.0)
    assert np.isfinite(loss)
