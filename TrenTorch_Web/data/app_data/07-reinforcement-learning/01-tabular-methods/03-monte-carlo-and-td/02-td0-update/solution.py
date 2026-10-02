import numpy as np


def td0_update(V: np.ndarray, state: int, reward: float, next_state: int,
               alpha: float, gamma: float, done: bool = False) -> np.ndarray:
    new_V = np.array(V, dtype=float)
    target = reward + (0.0 if done else gamma * new_V[next_state])
    new_V[state] += alpha * (target - new_V[state])
    return new_V
