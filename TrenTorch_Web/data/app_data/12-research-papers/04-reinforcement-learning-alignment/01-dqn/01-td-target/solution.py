def td_target(r, gamma, max_next_q, done):
    return r + gamma * (1 - done) * max_next_q
