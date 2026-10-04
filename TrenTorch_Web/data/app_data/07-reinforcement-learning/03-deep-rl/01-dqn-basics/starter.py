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
    pass
