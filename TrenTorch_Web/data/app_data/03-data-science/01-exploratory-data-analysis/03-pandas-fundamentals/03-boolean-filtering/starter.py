import pandas as pd


def in_range(df: pd.DataFrame, column: str, low, high) -> pd.DataFrame:
    """Rows where low <= df[column] <= high. NaN rows are dropped."""
    # TODO: Build the mask and select the rows.
    pass


def from_cities_and_old_enough(df: pd.DataFrame, cities, min_age) -> pd.DataFrame:
    """Rows whose city is in `cities` AND whose age >= min_age."""
    # TODO: Combine two conditions.
    pass


def any_extreme(df: pd.DataFrame, column: str, low, high) -> pd.DataFrame:
    """Rows where column < low OR column > high. NaN is not extreme (dropped)."""
    # TODO: Combine two conditions with "or".
    pass


def exclude_values(df: pd.DataFrame, column: str, values) -> pd.DataFrame:
    """Rows whose column is NOT in `values`. A NaN row is kept."""
    # TODO: Negate a membership test.
    pass


def complete_rows(df: pd.DataFrame, columns) -> pd.DataFrame:
    """Rows with no missing value in any of the listed columns."""
    # TODO: Require every listed column to be present.
    pass
