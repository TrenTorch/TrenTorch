import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def histogram_axes(df: pd.DataFrame, column: str, bins: int, stat: str):
    return sns.histplot(data=df, x=column, bins=bins, stat=stat)


def kde_axes(df: pd.DataFrame, column: str):
    return sns.kdeplot(data=df, x=column)


def kde_by_group(df: pd.DataFrame, column: str, group: str, order: list):
    return sns.kdeplot(data=df, x=column, hue=group, hue_order=order, common_norm=False)


def ecdf_axes(df: pd.DataFrame, column: str):
    return sns.ecdfplot(data=df, x=column)
