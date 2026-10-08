import math


def cosine_lr(t_cur, T_i, eta_min, eta_max):
    return eta_min + 0.5 * (eta_max - eta_min) * (1 + math.cos(math.pi * t_cur / T_i))
