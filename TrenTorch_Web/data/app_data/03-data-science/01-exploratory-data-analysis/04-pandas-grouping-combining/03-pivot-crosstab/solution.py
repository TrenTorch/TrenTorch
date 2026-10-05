import pandas as pd


def revenue_pivot(df: pd.DataFrame) -> pd.DataFrame:
    grid = df.pivot_table(index="region", columns="quarter", values="revenue", aggfunc="sum", fill_value=0)
    return grid.sort_index(axis=0).sort_index(axis=1)


def add_totals(grid: pd.DataFrame) -> pd.DataFrame:
    out = grid.copy()
    out["Total"] = out.sum(axis=1)
    out.loc["Total"] = out.sum(axis=0)
    return out


def count_table(df: pd.DataFrame, row: str, col: str) -> pd.DataFrame:
    return pd.crosstab(df[row], df[col])


def row_percentages(table: pd.DataFrame) -> pd.DataFrame:
    totals = table.sum(axis=1).astype(float)
    totals = totals.where(totals != 0)
    return table.div(totals, axis=0) * 100


def to_long(wide: pd.DataFrame, id_col: str, var_name: str, value_name: str) -> pd.DataFrame:
    order = {value: position for position, value in enumerate(wide[id_col])}
    long = wide.melt(id_vars=[id_col], var_name=var_name, value_name=value_name)
    long = long.sort_values(id_col, key=lambda s: s.map(order), kind="mergesort")
    return long.reset_index(drop=True)
