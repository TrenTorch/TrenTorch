import numpy as np


def ddpg_critic_target(r, gamma, done, q_next):
    return r + gamma * (1 - done) * q_next
