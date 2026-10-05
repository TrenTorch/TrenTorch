import pandas as pd


def parse_dates(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")


def calendar_features(dates: pd.Series) -> pd.DataFrame:
    out = pd.DataFrame(index=dates.index)
    out["year"] = dates.dt.year.astype(int)
    out["month"] = dates.dt.month.astype(int)
    out["dayofweek"] = dates.dt.dayofweek.astype(int)
    out["is_weekend"] = out["dayofweek"] >= 5
    return out


def monthly_total(df: pd.DataFrame, date_col: str, value_col: str) -> pd.Series:
    series = df.set_index(date_col)[value_col]
    return series.resample("MS").sum().rename(value_col)


def rolling_average(s: pd.Series, window: int) -> pd.Series:
    return s.rolling(window).mean()


def days_between(start: pd.Series, end: pd.Series) -> pd.Series:
    return (end - start).dt.days.astype(int)
