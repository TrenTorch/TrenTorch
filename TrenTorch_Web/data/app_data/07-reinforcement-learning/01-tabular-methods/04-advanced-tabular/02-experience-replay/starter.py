from collections import deque
import numpy as np


class ExperienceReplayBuffer:
    """Experience replay buffer for off-policy learning."""

    def __init__(self, capacity):
        """
        Initialize replay buffer.

        Args:
            capacity: max number of transitions to store
        """
        pass

    def add(self, state, action, reward, next_state, done):
        """Add transition to buffer."""
        pass

    def sample(self, batch_size):
        """Sample random batch of transitions."""
        pass

    def __len__(self):
        """Current buffer size."""
        pass
