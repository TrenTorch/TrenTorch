import numpy as np


def bellman_backup(V: np.ndarray, P: np.ndarray, R: np.ndarray, gamma: float):
    num_states, num_actions, _ = P.shape
    Q = np.zeros((num_states, num_actions))
    for s in range(num_states):
        for a in range(num_actions):
            Q[s, a] = np.sum(P[s, a] * (R[s, a] + gamma * V))
    return Q.max(axis=1), Q


def value_iteration(P: np.ndarray, R: np.ndarray, gamma: float, theta: float = 1e-8, max_iterations: int = 10000):
    num_states = P.shape[0]
    V = np.zeros(num_states)
    Q = None
    for _ in range(max_iterations):
        new_V, Q = bellman_backup(V, P, R, gamma)
        delta = np.max(np.abs(new_V - V))
        V = new_V
        if delta < theta:
            break
    policy = np.argmax(Q, axis=1)
    return V, policy


def policy_evaluation_exact(policy: np.ndarray, P: np.ndarray, R: np.ndarray, gamma: float) -> np.ndarray:
    num_states = P.shape[0]
    P_pi = np.array([P[s, policy[s]] for s in range(num_states)])
    R_pi = np.array([np.sum(P[s, policy[s]] * R[s, policy[s]]) for s in range(num_states)])
    A = np.eye(num_states) - gamma * P_pi
    return np.linalg.solve(A, R_pi)
