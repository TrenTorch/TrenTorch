import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
a3c_losses = _module.a3c_losses


def test_basic_losses():
    """Basic A3C losses."""
    log_probs = [-0.5, -1.0]
    values = [1.0, 2.0]
    next_values = [0.5, 1.0]
    actions = [0, 1]
    rewards = [1.0, 2.0]

    actor_loss, critic_loss, entropy = a3c_losses(log_probs, values, next_values, actions, rewards, gamma=0.99)

    assert isinstance(actor_loss, (float, np.floating))
    assert isinstance(critic_loss, (float, np.floating))
    assert isinstance(entropy, (float, np.floating))
    assert entropy > 0


def test_entropy_regularization():
    """Entropy regularization reduces actor loss."""
    log_probs = [-0.5, -0.5]
    values = [1.0, 1.0]
    next_values = [0.0, 0.0]
    actions = [0, 0]
    rewards = [1.0, 1.0]

    loss_no_entropy = a3c_losses(log_probs, values, next_values, actions, rewards, gamma=0.0, entropy_coeff=0.0)[0]
    loss_with_entropy = a3c_losses(log_probs, values, next_values, actions, rewards, gamma=0.0, entropy_coeff=0.1)[0]

    # Entropy bonus reduces actor loss
    assert loss_with_entropy < loss_no_entropy


def test_zero_advantage():
    """Zero advantage gives small actor loss."""
    log_probs = [-0.5, -0.5]
    values = [1.0, 2.0]
    next_values = [1.0, 2.0]  # Perfect predictions
    actions = [0, 0]
    rewards = [1.0, 2.0]

    actor_loss, critic_loss, _ = a3c_losses(log_probs, values, next_values, actions, rewards, gamma=0.0)

    # Critic loss should be nearly zero
    assert np.isclose(critic_loss, 0.0, atol=1e-5)


def test_high_entropy():
    """High entropy coefficient boosts entropy regularization."""
    log_probs = [-0.5]
    values = [1.0]
    next_values = [0.0]
    actions = [0]
    rewards = [1.0]

    loss1 = a3c_losses(log_probs, values, next_values, actions, rewards, gamma=0.0, entropy_coeff=0.0)[0]
    loss2 = a3c_losses(log_probs, values, next_values, actions, rewards, gamma=0.0, entropy_coeff=1.0)[0]

    # Higher entropy coeff should reduce loss more
    assert loss2 < loss1
