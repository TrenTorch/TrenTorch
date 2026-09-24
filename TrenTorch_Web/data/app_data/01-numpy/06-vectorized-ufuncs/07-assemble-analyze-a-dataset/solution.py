import numpy as np


def analyze_dataset(data: np.ndarray, lower_bound: float, upper_bound: float) -> dict:
    transformed = np.sqrt(np.abs(data))
    valid_mask = (transformed > lower_bound) & (transformed < upper_bound)
    valid_count = int(valid_mask.sum())
    feature_means = transformed.mean(axis=0)
    sample_maxes = transformed.max(axis=1)

    return {
        "transformed": transformed,
        "valid_mask": valid_mask,
        "valid_count": valid_count,
        "feature_means": feature_means,
        "sample_maxes": sample_maxes,
    }
