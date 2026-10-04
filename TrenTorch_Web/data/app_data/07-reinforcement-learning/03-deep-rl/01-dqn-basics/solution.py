import numpy as np


def dqn_loss(q_predictions, actions, rewards, next_q_target, done, gamma=0.99):
    """
    DQN loss (Huber loss with target network).

    Args:
        q_predictions: shape (batch,) - Q values for selected actions
        actions: shape (batch,) - action indices
        rewards: shape (batch,) - immediate rewards
        next_q_target: shape (batch,) - max Q' from target network
        done: shape (batch,) - terminal flags
        gamma: discount factor

    Returns:
        loss: scalar loss value
    """
    q_predictions = np.array(q_predictions, dtype=np.float32)
    rewards = np.array(rewards, dtype=np.float32)
    next_q_target = np.array(next_q_target, dtype=np.float32)
    done = np.array(done, dtype=np.float32)

    # Compute target
    target = rewards + gamma * next_q_target * (1 - done)

    # TD error
    td_error = target - q_predictions

    # Huber loss
    huber_loss = np.where(
        np.abs(td_error) <= 1.0,
        0.5 * td_error ** 2,
        np.abs(td_error) - 0.5
    )

    loss = np.mean(huber_loss)

    return float(loss)
