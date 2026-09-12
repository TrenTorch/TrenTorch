import numpy as np


def xavier_uniform_bound(fan_in: int, fan_out: int) -> float:
    return np.sqrt(6.0 / (fan_in + fan_out))


def xavier_normal_std(fan_in: int, fan_out: int) -> float:
    return np.sqrt(2.0 / (fan_in + fan_out))


def kaiming_uniform_bound(fan_in: int, gain: float = np.sqrt(2.0)) -> float:
    return gain * np.sqrt(3.0 / fan_in)


def kaiming_normal_std(fan_in: int, gain: float = np.sqrt(2.0)) -> float:
    return gain / np.sqrt(fan_in)
