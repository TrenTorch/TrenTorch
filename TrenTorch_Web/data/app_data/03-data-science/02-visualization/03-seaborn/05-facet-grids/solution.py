import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def histograms_by_group(df: pd.DataFrame, value: str, col: str, col_order: list, bins: int):
    return sns.displot(data=df, x=value, col=col, col_order=col_order, bins=bins)


def bars_by_group(df: pd.DataFrame, x: str, y: str, col: str, col_order: list):
    return sns.catplot(data=df, x=x, y=y, col=col, col_order=col_order, kind="bar", errorbar=None)


def pair_scatter(df: pd.DataFrame, variables: list):
    return sns.pairplot(df, vars=variables)
