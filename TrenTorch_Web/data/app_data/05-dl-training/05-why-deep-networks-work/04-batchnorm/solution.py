import numpy as np


def batchnorm_forward(
    x: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    running_mean: np.ndarray,
    running_var: np.ndarray,
    momentum: float = 0.1,
    eps: float = 1e-5,
    training: bool = True,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if training:
        n = x.shape[0]
        batch_mean = x.mean(axis=0)
        batch_var = x.var(axis=0)

        x_norm = (x - batch_mean) / np.sqrt(batch_var + eps)
        out = gamma * x_norm + beta

        batch_var_unbiased = batch_var * n / (n - 1)
        running_mean = (1.0 - momentum) * running_mean + momentum * batch_mean
        running_var = (1.0 - momentum) * running_var + momentum * batch_var_unbiased
    else:
        x_norm = (x - running_mean) / np.sqrt(running_var + eps)
        out = gamma * x_norm + beta

    return out, running_mean, running_var
