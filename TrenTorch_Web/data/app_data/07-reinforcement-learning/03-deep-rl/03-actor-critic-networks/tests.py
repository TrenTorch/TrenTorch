import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
actor_critic_losses = _module.actor_critic_losses


def test_basic_losses():
    """Basic AC losses."""
    log_probs = [-0.5, -1.0, -0.3]
    values = [1.0, 2.0, 0.5]
    actions = [0, 1, 0]
    rewards = [1.0, 2.0, 3.0]
    next_values = [0.5, 1.0, 2.0]

    actor_loss, critic_loss = actor_critic_losses(log_probs, values, actions, rewards, next_values, gamma=0.99)

    assert isinstance(actor_loss, (float, np.floating))
    assert isinstance(critic_loss, (float, np.floating))
    assert actor_loss > 0
    assert critic_loss >= 0


def test_perfect_values():
    """Perfect value predictions give low critic loss."""
    log_probs = [-0.5, -0.5]
    values = [1.0, 2.0]  # Perfect predictions
    actions = [0, 0]
    rewards = [1.0, 2.0]
    next_values = [0.0, 0.0]

    _, critic_loss = actor_critic_losses(log_probs, values, actions, rewards, next_values, gamma=0.0)

    assert np.isclose(critic_loss, 0.0)


def test_advantage_reduces_variance():
    """Advantage baseline reduces actor loss variance."""
    log_probs = [-1.0, -1.0]
    values = [5.0, 5.0]  # High baseline
    actions = [0, 0]
    rewards = [10.0, 10.0]
    next_values = [0.0, 0.0]

    actor_loss, _ = actor_critic_losses(log_probs, values, actions, rewards, next_values, gamma=0.0)

    # Should use advantage = 10 - 5 = 5
    assert actor_loss > 0


def test_different_gamma():
    """Different gamma values."""
    log_probs = [-0.5]
    values = [1.0]
    actions = [0]
    rewards = [1.0]
    next_values = [1.0]

    loss1 = actor_critic_losses(log_probs, values, actions, rewards, next_values, gamma=0.0)[1]
    loss2 = actor_critic_losses(log_probs, values, actions, rewards, next_values, gamma=0.99)[1]

    assert not np.isclose(loss1, loss2)


def test_negative_advantage():
    """Negative advantage (bad action) increases actor loss."""
    log_probs = [-1.0]
    values = [10.0]  # High value estimate
    actions = [0]
    rewards = [1.0]  # Low reward
    next_values = [0.0]

    actor_loss, _ = actor_critic_losses(log_probs, values, actions, rewards, next_values, gamma=0.0)

    # Negative advantage should increase loss
    assert actor_loss > 0
