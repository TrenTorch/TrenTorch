import numpy as np


def clean_and_reorder(data: np.ndarray, row_range: tuple, priority_indices: list) -> dict:
    """
    `data` is a 2D array. `row_range` is a (start, stop) tuple.
    `priority_indices` is a list of column indices.

    Perform the following steps, in order:
      1. Extract the sub-region of `data` spanning rows
         row_range[0] to row_range[1] (exclusive), all columns,
         using slicing. Call this `region`.
      2. Within `region`, treat any value less than 0 as invalid.
         Using np.where, produce a cleaned version of `region`
         where every invalid value is replaced with 0, and all
         other values are kept as-is. Call this `cleaned`.
         Do NOT mutate `region` or `data` in this step.
      3. From `cleaned`, extract the columns listed in
         `priority_indices`, in the exact order given (which may
         reorder columns), using fancy indexing on the column
         axis. Call this `reordered`.

    Return a dictionary:
      {
        "region": region,
        "cleaned": cleaned,
        "reordered": reordered,
        "region_shares_memory_with_data": <True if mutating
            `region` would affect `data`, False otherwise>,
        "cleaned_shares_memory_with_region": <True if mutating
            `cleaned` would affect `region`, False otherwise>
      }
    """
    pass
