import pandas as pd


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.isna().sum()
    counts = counts[counts > 0]
    out = pd.DataFrame(
        {
            "n_missing": counts.astype(int),
            "pct": (100.0 * counts / len(df)).round(1),
        }
    )
    out = out.sort_index()
    return out.sort_values("n_missing", ascending=False, kind="mergesort")


def fill_group_median(df: pd.DataFrame, key: str, column: str) -> pd.Series:
    values = df[column].astype(float)
    group_median = values.groupby(df[key]).transform("median")
    return values.fillna(group_median).fillna(values.median())


def forward_fill_limit(s: pd.Series, limit: int) -> pd.Series:
    return s.ffill(limit=limit)


def drop_sparse_columns(df: pd.DataFrame, max_missing_fraction: float) -> pd.DataFrame:
    keep = df.columns[df.isna().mean() <= max_missing_fraction]
    return df[keep]


def fill_with_indicator(df: pd.DataFrame, column: str) -> pd.DataFrame:
    out = df.copy()
    out[column + "_was_missing"] = df[column].isna()
    out[column] = df[column].fillna(df[column].median())
    return out
