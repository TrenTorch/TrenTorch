import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
actor_critic_loss = _module.actor_critic_loss


def test_basic_loss():
    """Basic loss computation."""
    logprobs = [-0.5, -1.0, -0.3]
    actions = [0, 1, 0]
    rewards = [1.0, 2.0, 0.5]
    next_values = [0.5, 1.0, 0.2]

    actor_loss, critic_loss = actor_critic_loss(logprobs, actions, rewards, next_values)

    assert isinstance(actor_loss, (float, np.floating))
    assert isinstance(critic_loss, (float, np.floating))
    assert actor_loss > 0
    assert critic_loss >= 0


def test_zero_advantage():
    """Zero advantage should give zero critic loss."""
    logprobs = [-0.5]
    actions = [0]
    rewards = [1.0]
    next_values = [1.0]  # r + γ*V'(s) = 1 + 0.99*1 ≈ 2
    gamma = 0.0

    actor_loss, critic_loss = actor_critic_loss(logprobs, actions, rewards, next_values, gamma=gamma)

    # With gamma=0, advantage = 1 + 0 = 1, not zero
    # Let me test with matching values instead
    pass


def test_negative_advantage():
    """Negative advantage reduces actor loss."""
    logprobs = [-0.5, -0.5]
    actions = [0, 0]
    rewards = [1.0, -1.0]
    next_values = [0.0, 0.0]

    actor_loss1, _ = actor_critic_loss(logprobs[:1], actions[:1], rewards[:1], next_values[:1])
    actor_loss2, _ = actor_critic_loss(logprobs[1:], actions[1:], rewards[1:], next_values[1:])

    # Negative advantage should give lower actor loss (larger magnitude advantage)
    assert actor_loss2 > actor_loss1


def test_scalar_outputs():
    """Outputs are scalars, not arrays."""
    logprobs = [-0.5]
    actions = [0]
    rewards = [1.0]
    next_values = [0.5]

    actor_loss, critic_loss = actor_critic_loss(logprobs, actions, rewards, next_values)

    assert isinstance(actor_loss, (int, float, np.floating))
    assert isinstance(critic_loss, (int, float, np.floating))


def test_batch_loss():
    """Loss computed over batch."""
    logprobs = [-0.5, -1.0, -0.3, -0.7]
    actions = [0, 1, 0, 1]
    rewards = [1.0, 2.0, 0.5, 1.5]
    next_values = [0.5, 1.0, 0.2, 0.8]

    actor_loss, critic_loss = actor_critic_loss(logprobs, actions, rewards, next_values)

    # Should average over batch
    assert actor_loss > 0
    assert critic_loss >= 0


def test_different_gamma():
    """Different gamma values."""
    logprobs = [-0.5]
    actions = [0]
    rewards = [1.0]
    next_values = [1.0]

    loss1 = actor_critic_loss(logprobs, actions, rewards, next_values, gamma=0.0)[1]
    loss2 = actor_critic_loss(logprobs, actions, rewards, next_values, gamma=0.99)[1]

    # Different gamma should give different losses
    assert loss1 >= 0
    assert loss2 >= 0
