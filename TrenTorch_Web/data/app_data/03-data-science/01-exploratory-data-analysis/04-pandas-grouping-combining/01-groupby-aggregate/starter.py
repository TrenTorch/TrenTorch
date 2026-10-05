import pandas as pd


def group_summary(df: pd.DataFrame, key: str, value: str) -> pd.DataFrame:
    """
    One row per distinct key (sorted ascending), columns n, mean, median, max
    of `value` (missing ignored; n counts the known values).
    """
    # TODO: Aggregate each group.
    pass


def add_group_mean(df: pd.DataFrame, key: str, value: str) -> pd.DataFrame:
    """A copy of df plus the column "<value>_group_mean" (mean over the row's group)."""
    # TODO: Attach each group's mean to its members.
    pass


def zscore_within_group(df: pd.DataFrame, key: str, value: str) -> pd.Series:
    """
    (value - group mean) / group sample std, float Series with df's index.
    NaN for a missing value, a group of one, std 0, or a missing key.
    """
    # TODO: Standardise within each group.
    pass


def top_n_per_group(df: pd.DataFrame, key: str, value: str, n: int) -> pd.DataFrame:
    """
    The n largest-`value` rows of each key (ties keep input order), ordered by
    key ascending then value descending. All columns, original index labels.
    """
    # TODO: Sort, take the head of each group, order the output.
    pass
