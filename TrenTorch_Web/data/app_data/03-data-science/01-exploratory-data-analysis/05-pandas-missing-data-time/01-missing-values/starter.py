import pandas as pd


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Only columns with missing values; columns n_missing (int) and pct (rounded
    to 1 decimal). Ordered by n_missing descending, ties by column name.
    """
    # TODO: Count and describe the holes.
    pass


def fill_group_median(df: pd.DataFrame, key: str, column: str) -> pd.Series:
    """
    df[column] with each missing value replaced by the median of the known
    values in its group; whole-column median if the group has none or the key
    is missing. Float Series with df's index.
    """
    # TODO: Group median first, overall median for what is left.
    pass


def forward_fill_limit(s: pd.Series, limit: int) -> pd.Series:
    """Carry the last known value forward into at most `limit` missing positions."""
    # TODO: Forward fill with a limit.
    pass


def drop_sparse_columns(df: pd.DataFrame, max_missing_fraction: float) -> pd.DataFrame:
    """Drop columns whose missing fraction is greater than max_missing_fraction."""
    # TODO: Keep the columns that are complete enough.
    pass


def fill_with_indicator(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    A copy with `column` filled by its median and a new boolean column
    "<column>_was_missing" (last) marking the filled rows.
    """
    # TODO: Record the holes, then fill them.
    pass
