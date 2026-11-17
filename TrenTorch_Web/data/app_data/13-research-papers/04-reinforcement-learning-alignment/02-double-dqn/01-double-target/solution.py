import numpy as np


def double_q_target(r, gamma, done, q_next_online, q_next_target):
    a = int(np.argmax(q_next_online))
    return r + gamma * (1 - done) * q_next_target[a]
