import pandas as pd


def rows_by_label(df: pd.DataFrame, start, stop) -> pd.DataFrame:
    return df.loc[start:stop]


def rows_by_position(df: pd.DataFrame, start: int, stop: int) -> pd.DataFrame:
    return df.iloc[start:stop]


def cell(df: pd.DataFrame, row_label, column):
    return df.at[row_label, column]


def numeric_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include="number").columns.tolist()


def with_value_where(df: pd.DataFrame, mask, column, value) -> pd.DataFrame:
    out = df.copy()
    out.loc[mask, column] = value
    return out
