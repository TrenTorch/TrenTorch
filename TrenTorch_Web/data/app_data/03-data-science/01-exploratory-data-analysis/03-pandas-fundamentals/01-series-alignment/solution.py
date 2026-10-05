import numpy as np
import pandas as pd


def make_series(values, labels, name) -> pd.Series:
    return pd.Series(list(values), index=list(labels), name=name)


def aligned_sum(a: pd.Series, b: pd.Series, fill_value=None) -> pd.Series:
    if fill_value is None:
        total = a + b
    else:
        total = a.add(b, fill_value=fill_value)
    return total.sort_index()


def share_of_total(s: pd.Series) -> pd.Series:
    s = s.astype(float)
    return s / s.sum()


def lookup(s: pd.Series, labels) -> pd.Series:
    return s.reindex(list(labels))
