import numpy as np
import pandas as pd

df = pd.DataFrame(
    {
        "city": ["a", "a", "b", "b", "c", None, "a", "b"],
        "income": [10.0, np.nan, 30.0, 50.0, np.nan, 40.0, 20.0, np.nan],
        "age": [25, 30, np.nan, 41, 52, 19, 33, 28],
    }
)
print("missing_report:")
print(missing_report(df))
print("\nincome filled with the median of its city:")
print(fill_group_median(df, "city", "income").tolist())
print("\nforward fill, at most 1 step:")
print(forward_fill_limit(pd.Series([1.0, np.nan, np.nan, 4.0]), 1).tolist())
print("\ncolumns with at most 20% missing:")
print(drop_sparse_columns(df, 0.2).columns.tolist())
print("\nfill_with_indicator('age'):")
print(fill_with_indicator(df, "age"))
