import pandas as pd


def in_range(df: pd.DataFrame, column: str, low, high) -> pd.DataFrame:
    return df[df[column].between(low, high)]


def from_cities_and_old_enough(df: pd.DataFrame, cities, min_age) -> pd.DataFrame:
    return df[df["city"].isin(list(cities)) & (df["age"] >= min_age)]


def any_extreme(df: pd.DataFrame, column: str, low, high) -> pd.DataFrame:
    return df[(df[column] < low) | (df[column] > high)]


def exclude_values(df: pd.DataFrame, column: str, values) -> pd.DataFrame:
    return df[~df[column].isin(list(values))]


def complete_rows(df: pd.DataFrame, columns) -> pd.DataFrame:
    return df[df[list(columns)].notna().all(axis=1)]
