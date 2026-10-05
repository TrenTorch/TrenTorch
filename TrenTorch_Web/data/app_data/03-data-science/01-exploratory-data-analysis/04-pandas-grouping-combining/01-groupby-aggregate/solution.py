import pandas as pd


def group_summary(df: pd.DataFrame, key: str, value: str) -> pd.DataFrame:
    out = df.groupby(key)[value].agg(n="count", mean="mean", median="median", max="max")
    return out.sort_index()


def add_group_mean(df: pd.DataFrame, key: str, value: str) -> pd.DataFrame:
    out = df.copy()
    out[f"{value}_group_mean"] = df.groupby(key)[value].transform("mean")
    return out


def zscore_within_group(df: pd.DataFrame, key: str, value: str) -> pd.Series:
    grouped = df.groupby(key)[value]
    mean = grouped.transform("mean")
    std = grouped.transform("std")
    z = (df[value].astype(float) - mean) / std
    return z.where(std > 0)


def top_n_per_group(df: pd.DataFrame, key: str, value: str, n: int) -> pd.DataFrame:
    known = df.dropna(subset=[key, value])
    ordered = known.sort_values(value, ascending=False, kind="mergesort")
    picked = ordered.groupby(key, sort=False).head(n)
    return picked.sort_values(key, kind="mergesort")
