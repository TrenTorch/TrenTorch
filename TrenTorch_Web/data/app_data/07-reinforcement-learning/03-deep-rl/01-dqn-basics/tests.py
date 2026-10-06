import numpy as np

from _load import load_solution

_module = load_solution(__file__)
dqn_loss = _module.dqn_loss


def test_basic_loss():
    """Basic DQN loss."""
    q_pred = [1.0, 2.0, 3.0]
    actions = [0, 1, 0]
    rewards = [1.0, 2.0, 3.0]
    next_q = [1.0, 2.0, 3.0]
    done = [0, 0, 0]

    loss = dqn_loss(q_pred, actions, rewards, next_q, done, gamma=0.99)

    assert isinstance(loss, (float, np.floating))
    assert loss >= 0


def test_perfect_prediction():
    """Perfect prediction gives zero loss."""
    rewards = [1.0, 2.0, 3.0]
    next_q = [0.0, 0.0, 0.0]
    q_pred = [1.0, 2.0, 3.0]
    done = [1, 1, 1]  # Terminal, so target = reward

    loss = dqn_loss(q_pred, [0]*3, rewards, next_q, done, gamma=0.99)

    assert np.isclose(loss, 0.0)


def test_terminal_state():
    """Terminal states have target = reward."""
    q_pred = [0.0]
    actions = [0]
    rewards = [1.0]
    next_q = [100.0]  # Ignored because done=1
    done = [1]

    loss = dqn_loss(q_pred, actions, rewards, next_q, done, gamma=0.99)

    # Loss should be based on |0 - 1| = 1
    assert loss > 0


def test_non_terminal_state():
    """Non-terminal states use next Q."""
    q_pred = [0.0]
    actions = [0]
    rewards = [0.0]
    next_q = [1.0]
    done = [0]

    loss = dqn_loss(q_pred, actions, rewards, next_q, done, gamma=1.0)

    # Target = 0 + 1 * 1 = 1, loss = Huber(1 - 0) = 0.5
    assert np.isclose(loss, 0.5)


def test_batch_averaging():
    """Loss is averaged over batch."""
    q_pred = [0.0, 0.0]
    actions = [0, 0]
    rewards = [1.0, 2.0]
    next_q = [0.0, 0.0]
    done = [1, 1]

    loss = dqn_loss(q_pred, actions, rewards, next_q, done, gamma=0.99)

    # Huber losses: [0.5, 2-0.5] = [0.5, 1.5], avg = 1.0
    assert np.isclose(loss, 1.0)


def test_different_gamma():
    """Different gamma values."""
    q_pred = [1.0]
    actions = [0]
    rewards = [1.0]
    next_q = [1.0]
    done = [0]

    loss1 = dqn_loss(q_pred, actions, rewards, next_q, done, gamma=0.0)
    loss2 = dqn_loss(q_pred, actions, rewards, next_q, done, gamma=0.99)

    # Different gamma should affect loss
    assert not np.isclose(loss1, loss2)
