import numpy as np


def epsilon_greedy_action(Q: np.ndarray, state: int, epsilon: float, rng: np.random.Generator) -> int:
    """
    With probability epsilon, picks a uniformly random action
    (exploration); otherwise picks the current best-known action,
    argmax(Q[state]) (exploitation).
    """
    # TODO: if rng.random() < epsilon, return a random action index
    # (rng.integers(Q.shape[1])); otherwise return int(np.argmax(Q[state])).
    pass


def q_learning_update(
    Q: np.ndarray, state: int, action: int, reward: float, next_state: int, alpha: float, gamma: float, done: bool
) -> np.ndarray:
    """
    The core tabular Q-learning (temporal-difference) update:
    Q[s, a] += alpha * (target - Q[s, a]), where target = reward if
    `done` (the episode ended, so there's no future value), otherwise
    reward + gamma * max_a' Q[next_state, a'] (bootstrapping off the
    CURRENT estimate of the best next action's value).
    """
    # TODO: compute best_next = 0.0 if done else Q[next_state].max().
    # td_target = reward + gamma * best_next. Update Q[state, action]
    # in place by alpha * (td_target - Q[state, action]). Return Q.
    pass


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
    """
    Runs model-free Q-learning against an MDP described the same way
    01-value-iteration-mdp's does (P, R as (num_states, num_actions,
    num_states) arrays) -- but WITHOUT ever looking at P or R directly
    to compute a value function; the agent only ever SAMPLES a single
    transition at a time (as if it didn't know the MDP's true dynamics
    at all) and learns purely from those samples.
    """
    # TODO: initialize Q as zeros((num_states, num_actions)) and a
    # rng = np.random.default_rng(seed). For num_episodes episodes:
    # start at a random state; while not in terminal_states, pick an
    # action via epsilon_greedy_action, sample next_state via
    # rng.choice(num_states, p=P[state, action]), look up reward =
    # R[state, action, next_state], set done = next_state in
    # terminal_states, call q_learning_update, then move to
    # next_state. Return Q.
    pass
