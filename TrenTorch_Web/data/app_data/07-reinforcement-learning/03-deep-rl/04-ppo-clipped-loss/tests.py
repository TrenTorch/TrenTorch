import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
ppo_loss = _module.ppo_loss


def test_basic_ppo():
    """Basic PPO loss."""
    log_probs_new = [-0.5, -1.0]
    log_probs_old = [-0.5, -1.0]
    advantages = [1.0, 2.0]

    loss = ppo_loss(log_probs_new, log_probs_old, advantages)

    assert isinstance(loss, (float, np.floating))
    assert loss >= 0


def test_identical_policies():
    """Identical old and new policies give zero loss."""
    log_probs_new = [-0.5, -0.5]
    log_probs_old = [-0.5, -0.5]
    advantages = [1.0, 2.0]

    loss = ppo_loss(log_probs_new, log_probs_old, advantages)

    # Ratio = 1, min(1*A, clip(1)*A) = A, loss = -mean(A)
    expected = -np.mean([1.0, 2.0])
    assert np.isclose(loss, expected)


def test_clipping_prevents_large_updates():
    """Large policy changes are clipped."""
    log_probs_new = [5.0]  # Much higher
    log_probs_old = [0.0]
    advantages = [1.0]

    loss_unclipped = ppo_loss([5.0], [0.0], [1.0], epsilon=1.0)
    loss_clipped = ppo_loss([5.0], [0.0], [1.0], epsilon=0.2)

    # Stricter clipping should give higher loss
    assert loss_clipped >= loss_unclipped


def test_negative_advantage():
    """Negative advantage reduces policy update."""
    log_probs_new = [0.0]
    log_probs_old = [0.0]
    advantages = [-1.0]

    loss = ppo_loss(log_probs_new, log_probs_old, advantages)

    # Loss should penalize the action
    assert loss > 0


def test_different_epsilon():
    """Different epsilon values affect clipping."""
    log_probs_new = [-1.0]
    log_probs_old = [-0.5]
    advantages = [1.0]

    loss1 = ppo_loss(log_probs_new, log_probs_old, advantages, epsilon=0.1)
    loss2 = ppo_loss(log_probs_new, log_probs_old, advantages, epsilon=0.5)

    assert not np.isclose(loss1, loss2)
