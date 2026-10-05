import pandas as pd


def parse_dates(s: pd.Series) -> pd.Series:
    """Parse 'YYYY-MM-DD' text to datetimes; anything invalid becomes NaT."""
    # TODO: Parse with an explicit format and no errors.
    pass


def calendar_features(dates: pd.Series) -> pd.DataFrame:
    """Columns year, month, dayofweek (Mon=0), is_weekend, with dates's index."""
    # TODO: Extract calendar parts.
    pass


def monthly_total(df: pd.DataFrame, date_col: str, value_col: str) -> pd.Series:
    """
    Sum of value_col per calendar month, indexed by month start, every month
    from first to last (empty months = 0), named value_col.
    """
    # TODO: Resample to months.
    pass


def rolling_average(s: pd.Series, window: int) -> pd.Series:
    """Mean of each value and the window-1 before it; first window-1 are NaN."""
    # TODO: Rolling mean over full windows.
    pass


def days_between(start: pd.Series, end: pd.Series) -> pd.Series:
    """Whole days from start to end (integer Series, negative if end is earlier)."""
    # TODO: Subtract and take whole days.
    pass
