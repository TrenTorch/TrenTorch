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
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        """Add transition to buffer."""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """Sample random batch of transitions."""
        batch_size = min(batch_size, len(self.buffer))
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)

        batch = [self.buffer[i] for i in indices]
        states, actions, rewards, next_states, dones = zip(*batch)

        return {
            'states': np.array(states),
            'actions': np.array(actions),
            'rewards': np.array(rewards),
            'next_states': np.array(next_states),
            'dones': np.array(dones)
        }

    def __len__(self):
        """Current buffer size."""
        return len(self.buffer)
