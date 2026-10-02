import numpy as np


def make_tensor(data, dtype: np.dtype | None = None) -> np.ndarray:
    """
    Mirrors torch.tensor(data, dtype=dtype)'s dtype-inference rule,
    which differs from NumPy's own default:
      - if dtype is given, cast to it, no inference needed.
      - otherwise, if the inferred dtype is floating-point, use
        float32 (PyTorch's real default float dtype), NOT NumPy's own
        default of float64.
      - otherwise (integers, bools), keep whatever NumPy inferred.
    """
    # TODO: np.array(data) first, then apply the rule above.
    pass


def zeros(shape: tuple[int, ...], dtype: np.dtype = np.float32) -> np.ndarray:
    """Mirrors torch.zeros(shape, dtype=dtype) -- PyTorch's own default dtype is float32."""
    # TODO: one line.
    pass


def ones(shape: tuple[int, ...], dtype: np.dtype = np.float32) -> np.ndarray:
    """Mirrors torch.ones(shape, dtype=dtype)."""
    # TODO: one line.
    pass


def arange(start: float, stop: float, step: float = 1, dtype: np.dtype | None = None) -> np.ndarray:
    """Mirrors torch.arange(start, stop, step, dtype=dtype), same float32-default rule as make_tensor."""
    # TODO: np.arange(start, stop, step), then the same dtype rule
    # make_tensor uses.
    pass
