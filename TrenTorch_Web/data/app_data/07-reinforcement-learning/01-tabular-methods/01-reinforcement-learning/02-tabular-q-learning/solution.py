import numpy as np


def epsilon_greedy_action(Q: np.ndarray, state: int, epsilon: float, rng: np.random.Generator) -> int:
    if rng.random() < epsilon:
        return int(rng.integers(Q.shape[1]))
    return int(np.argmax(Q[state]))


def q_learning_update(
    Q: np.ndarray, state: int, action: int, reward: float, next_state: int, alpha: float, gamma: float, done: bool
) -> np.ndarray:
    best_next = 0.0 if done else np.max(Q[next_state])
    td_target = reward + gamma * best_next
    Q[state, action] += alpha * (td_target - Q[state, action])
    return Q


def train_q_learning(
    P: np.ndarray,
    R: np.ndarray,
    terminal_states: set,
    gamma: float,
    num_episodes: int,
    alpha: float = 0.1,
    epsilon: float = 0.2,
    seed: int = 0,
) -> np.ndarray:
    num_states, num_actions, _ = P.shape
    Q = np.zeros((num_states, num_actions))
    rng = np.random.default_rng(seed)

    for _ in range(num_episodes):
        state = int(rng.integers(num_states))
        while state not in terminal_states:
            action = epsilon_greedy_action(Q, state, epsilon, rng)
            next_state = int(rng.choice(num_states, p=P[state, action]))
            reward = R[state, action, next_state]
            done = next_state in terminal_states
            Q = q_learning_update(Q, state, action, reward, next_state, alpha, gamma, done)
            state = next_state

    return Q
