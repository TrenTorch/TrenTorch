import pandas as pd


def sort_by_columns(df: pd.DataFrame, columns: list, ascending: list) -> pd.DataFrame:
    return df.sort_values(list(columns), ascending=list(ascending), kind="mergesort", na_position="last")


def rank_scores(s: pd.Series, method: str) -> pd.Series:
    return s.rank(method=method, ascending=False).astype(float)


def top_n(df: pd.DataFrame, column: str, n: int) -> pd.DataFrame:
    known = df.dropna(subset=[column])
    return known.sort_values(column, ascending=False, kind="mergesort").head(n)


def percent_rank(s: pd.Series) -> pd.Series:
    ranks = s.rank(method="min", ascending=True)
    return (ranks - 1) / (s.count() - 1)
