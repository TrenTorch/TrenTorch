import numpy as np


def cast_to_dtype(x: np.ndarray, dtype: str) -> np.ndarray:
    """
    x: a float32 array
    dtype: "float16" or "float32" (bfloat16 has no native NumPy dtype,
        so this exercise sticks to dtypes NumPy itself supports)

    Returns x cast to the given dtype -- NumPy's real IEEE-754 rounding
    behavior, not a simulation.
    """
    # TODO: x.astype(dtype).
    pass


def detect_underflow(original: np.ndarray, casted: np.ndarray) -> np.ndarray:
    """
    original: the array before casting
    casted: the same array after cast_to_dtype

    Returns a boolean mask, True wherever a genuinely nonzero value
    rounded all the way down to exactly zero after casting -- lost
    entirely, not just rounded imprecisely.
    """
    # TODO: elementwise (original != 0) AND (casted == 0).
    pass


def detect_overflow(casted: np.ndarray) -> np.ndarray:
    """
    casted: an array already cast to some narrower dtype

    Returns a boolean mask, True wherever casting pushed a finite value
    past the dtype's representable maximum, producing +-inf.
    """
    # TODO: np.isinf(casted).
    pass
