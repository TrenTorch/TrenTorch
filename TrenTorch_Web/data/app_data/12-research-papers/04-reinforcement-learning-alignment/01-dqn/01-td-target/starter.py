def td_target(r, gamma, max_next_q, done):
    """
    r: reward for the transition
    gamma: discount factor in [0, 1]
    max_next_q: max over actions of the target network's Q at the next state
    done: 1 if the episode ended, else 0

    Returns:
        The Bellman target r + gamma * (1 - done) * max_next_q.
    """
    # TODO: Return the one-step target, with no bootstrapping after a terminal state (see Theory).
    pass
