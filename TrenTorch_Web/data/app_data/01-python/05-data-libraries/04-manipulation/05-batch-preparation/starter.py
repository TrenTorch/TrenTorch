import numpy as np


def prepare_batch(
    flat_data: np.ndarray, batch_size: int, feature_count: int, num_groups: int
) -> dict:
    """
    `flat_data` is a 1D array whose length equals
    batch_size * feature_count.

    Perform the following steps, in order:
      1. Reshape flat_data into shape (batch_size, feature_count),
         calling the result `batch`.
      2. Transpose `batch` to shape (feature_count, batch_size),
         calling the result `transposed`.
      3. Add a new leading dimension of size 1 to `transposed`,
         producing shape (1, feature_count, batch_size), using
         np.newaxis or expand_dims. Call this `with_channel`.
      4. Split `with_channel` along its second axis (the
         feature_count axis) into `num_groups` equal parts,
         using np.split with the correct axis. Call this list
         `groups`.

    Return a dictionary:
      {
        "batch": batch,
        "transposed": transposed,
        "with_channel": with_channel,
        "groups": groups,
        "with_channel_shares_memory_with_flat_data": <bool>,
        "groups_first_shares_memory_with_flat_data": <bool>
      }

    Assume feature_count is evenly divisible by num_groups.
    """
    pass
