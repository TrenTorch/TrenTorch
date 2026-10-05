import numpy as np
import pandas as pd


def make_series(values, labels, name) -> pd.Series:
    """Returns a Series of `values` indexed by `labels` (same order), named `name`."""
    # TODO: Build the Series with its labels and name.
    pass


def aligned_sum(a: pd.Series, b: pd.Series, fill_value=None) -> pd.Series:
    """
    Adds a and b by label. The index is every label from either side, sorted
    ascending. A label missing from one side gives NaN. With fill_value, a
    missing label or NaN value on either side counts as fill_value, unless
    both sides are missing for that label (then NaN). Does not change a or b.
    """
    # TODO: Add the two Series by label and order the result.
    pass


def share_of_total(s: pd.Series) -> pd.Series:
    """
    Each value divided by the sum of the non-missing values. Missing values
    stay missing. Same index and name as s, float values.
    """
    # TODO: Divide by the total of the known values.
    pass


def lookup(s: pd.Series, labels) -> pd.Series:
    """
    Value of s for each label in `labels`, in that order, indexed by `labels`.
    A label that s does not have gives NaN instead of an error.
    """
    # TODO: Conform s to the requested labels.
    pass
