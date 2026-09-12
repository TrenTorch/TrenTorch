import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

correlation = load_solution("00-math-and-statistics/03-probability/03-covariance-correlation").correlation


def feature_target_correlations(x: np.ndarray, target: np.ndarray) -> np.ndarray:
    """
    x is (num_samples, num_features), target is (num_samples,). Returns
    a length-num_features array: each feature's correlation with the
    target, using the provided `correlation` function.
    """
    pass


def find_suspicious_features(x: np.ndarray, target: np.ndarray, threshold: float = 0.95) -> np.ndarray:
    """
    Returns the indices of every feature whose |correlation| with the
    target exceeds `threshold`, a first-pass, automatable check for
    the specific kind of data leakage where a feature accidentally
    encodes (or nearly encodes) the label itself.
    """
    pass
