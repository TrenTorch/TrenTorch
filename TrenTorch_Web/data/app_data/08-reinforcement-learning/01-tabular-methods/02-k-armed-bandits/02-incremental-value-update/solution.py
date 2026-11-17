import numpy as np


def update_action_value(q_values: np.ndarray, counts: np.ndarray, action: int, reward: float) -> tuple:
    q = np.array(q_values, dtype=float)
    n = np.array(counts, dtype=int)
    n[action] += 1
    q[action] += (reward - q[action]) / n[action]
    return q, n
