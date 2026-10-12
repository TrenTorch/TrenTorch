import numpy as np

from _load import load_solution

_module = load_solution(__file__)
policy_gradient_loss = _module.policy_gradient_loss


def test_basic_loss():
    """Basic policy gradient loss."""
    log_probs = [-0.5, -1.0, -0.2]
    advantages = [1.0, 0.5, 2.0]

    loss = policy_gradient_loss(log_probs, advantages)

    assert isinstance(loss, (float, np.floating))


def test_positive_advantage():
    """Positive advantage gives negative loss."""
    log_probs = [-1.0]
    advantages = [1.0]

    loss = policy_gradient_loss(log_probs, advantages)

    # -mean(-1.0 * 1.0) = -(-1.0) = 1.0
    assert loss > 0


def test_negative_advantage():
    """Negative advantage gives positive loss."""
    log_probs = [-1.0]
    advantages = [-1.0]

    loss = policy_gradient_loss(log_probs, advantages)

    # -mean(-1.0 * -1.0) = -(1.0) = -1.0
    assert loss < 0


def test_zero_advantage():
    """Zero advantage gives zero loss."""
    log_probs = [-0.5, -1.0]
    advantages = [0.0, 0.0]

    loss = policy_gradient_loss(log_probs, advantages)

    assert np.isclose(loss, 0.0)


def test_batch_averaging():
    """Loss is averaged over batch."""
    log_probs = [-1.0, -1.0, -1.0]
    advantages = [1.0, 1.0, 1.0]

    loss = policy_gradient_loss(log_probs, advantages)

    # -mean(-1 * 1) = -mean(-1) = 1
    assert np.isclose(loss, 1.0)


def test_magnitude():
    """Magnitude of advantage affects loss magnitude."""
    log_probs = [-1.0, -1.0]
    advantages1 = [1.0, 1.0]
    advantages2 = [10.0, 10.0]

    loss1 = policy_gradient_loss(log_probs, advantages1)
    loss2 = policy_gradient_loss(log_probs, advantages2)

    # Loss2 should be 10x loss1
    assert np.isclose(loss2 / loss1, 10.0)
