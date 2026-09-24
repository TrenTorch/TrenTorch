import numpy as np


def analyze_dataset(data: np.ndarray, lower_bound: float, upper_bound: float) -> dict:
    """
    `data` is a 2D array of shape (num_samples, num_features).

    Perform the following, using only vectorized operations
    (no explicit Python for loop over individual elements):

      1. Compute `transformed`: the element-wise square root of
         the absolute value of every element in `data` (use
         np.abs then np.sqrt).
      2. Build a boolean mask, `valid_mask`, that is True at
         every position in `transformed` where the value is
         between lower_bound and upper_bound (inclusive of
         neither bound — strictly between).
      3. Compute `valid_count`: the total number of True values
         in valid_mask across the whole array.
      4. Compute `feature_means`: the mean of `transformed` along
         axis 0 (the mean of each feature/column across all
         samples), producing a 1D array of length num_features.
      5. Compute `sample_maxes`: the maximum value in each row of
         `transformed` (i.e. along axis 1), producing a 1D array
         of length num_samples.

    Return a dictionary:
      {
        "transformed": transformed,
        "valid_mask": valid_mask,
        "valid_count": valid_count,
        "feature_means": feature_means,
        "sample_maxes": sample_maxes
      }
    """
    pass
