import numpy as np


def patch_rows(clean: np.ndarray, corrupt: np.ndarray, rows) -> np.ndarray:
    """Copy of `corrupt` with the given rows taken from `clean`."""
    # TODO
    pass


def recovery(clean_metric: float, corrupt_metric: float, patched_metric: float) -> float:
    """(patched - corrupt) / (clean - corrupt)."""
    # TODO
    pass


def patching_scan(model, clean: np.ndarray, corrupt: np.ndarray) -> np.ndarray:
    """Recovery fraction from patching each position of the corrupted run with the clean activation."""
    # TODO
    pass
