import math

import pandas as pd
from pandas.api import types as pdt


def profile(df: pd.DataFrame) -> dict:
    missing = {col: int(df[col].isna().sum()) for col in df.columns}
    numeric = {}
    categorical = {}
    for col in df.columns:
        s = df[col]
        if pdt.is_numeric_dtype(s) and not pdt.is_bool_dtype(s):
            known = s.dropna().astype(float)
            if len(known) == 0:
                numeric[col] = {"mean": math.nan, "std": math.nan, "min": math.nan, "max": math.nan}
            else:
                numeric[col] = {
                    "mean": float(known.mean()),
                    "std": float(known.std(ddof=1)) if len(known) > 1 else math.nan,
                    "min": float(known.min()),
                    "max": float(known.max()),
                }
        else:
            counts = s.dropna().value_counts()
            if counts.empty:
                categorical[col] = {"n_unique": 0, "top": None, "top_count": 0}
            else:
                best = counts.max()
                top = min(counts[counts == best].index.tolist())
                categorical[col] = {"n_unique": int(len(counts)), "top": top, "top_count": int(best)}
    return {
        "n_rows": int(len(df)),
        "n_cols": int(df.shape[1]),
        "missing": missing,
        "n_duplicate_rows": int(df.duplicated().sum()),
        "numeric": numeric,
        "categorical": categorical,
    }
