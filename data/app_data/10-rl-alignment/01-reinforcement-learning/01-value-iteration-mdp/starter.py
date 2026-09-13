import numpy as np


def bellman_backup(V: np.ndarray, P: np.ndarray, R: np.ndarray, gamma: float):
    """
    One Bellman optimality backup: for every state s and action a,
    Q[s, a] = sum_{s'} P[s, a, s'] * (R[s, a, s'] + gamma * V[s']).
    Returns (new_V, Q), where new_V[s] = max_a Q[s, a].

    P has shape (num_states, num_actions, num_states) -- P[s, a, s']
    is the probability of landing in s' after taking action a in
    state s. R has the same shape -- R[s, a, s'] is the reward for
    that specific transition.
    """
    # TODO: for each s, a, compute Q[s, a] = np.sum(P[s, a] * (R[s, a]
    # + gamma * V)). Return (Q.max(axis=1), Q).
    pass


def value_iteration(P: np.ndarray, R: np.ndarray, gamma: float, theta: float = 1e-8, max_iterations: int = 10000):
    """
    Repeatedly applies bellman_backup, starting from V = 0, until the
    largest change in any state's value drops below theta (or
    max_iterations is hit). Returns (V, policy), where policy[s] is
    the argmax action for state s under the converged V.
    """
    # TODO: loop bellman_backup, tracking the max |new_V - V| each
    # iteration, breaking once it's below theta. Extract policy as
    # Q.argmax(axis=1) from the LAST Q computed.
    pass


def policy_evaluation_exact(policy: np.ndarray, P: np.ndarray, R: np.ndarray, gamma: float) -> np.ndarray:
    """
    Solves for a GIVEN policy's true value function exactly, via
    linear algebra rather than iteration: V = (I - gamma * P_pi)^-1 @
    R_pi, where P_pi/R_pi are P/R restricted to the actions `policy`
    actually takes in each state. Used as an independent correctness
    check on value_iteration's output.
    """
    # TODO: build P_pi[s] = P[s, policy[s]] and R_pi[s] = sum(P[s,
    # policy[s]] * R[s, policy[s]]) for every state s, then
    # np.linalg.solve(np.eye(num_states) - gamma * P_pi, R_pi).
    pass
