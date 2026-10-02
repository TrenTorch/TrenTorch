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
    """
    Batch normalization's forward pass. `x` has shape (batch_size,
    num_features). `gamma`/`beta` are learnable per-feature scale/shift
    parameters (shape (num_features,)). `running_mean`/`running_var` are
    exponential moving averages of the mean/variance seen during
    training, used INSTEAD of the current batch's own statistics when
    `training=False`.

    TRAINING mode: normalize `x` using THIS batch's own mean and
    (biased) variance, then update running_mean/running_var with an
    exponential moving average (using the batch's UNBIASED variance for
    that specific update, matching torch.nn.BatchNorm1d exactly).

    EVAL mode: normalize `x` using the stored running_mean/running_var
    directly (no batch statistics computed at all), and leave
    running_mean/running_var unchanged.

    Returns (output, updated_running_mean, updated_running_var).
    """
    pass
