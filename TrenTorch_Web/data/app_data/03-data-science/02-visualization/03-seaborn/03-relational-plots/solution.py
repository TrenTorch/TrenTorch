import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def scatter_by_group(df: pd.DataFrame, x: str, y: str, hue: str, hue_order: list):
    return sns.scatterplot(data=df, x=x, y=y, hue=hue, hue_order=hue_order)


def mean_line(df: pd.DataFrame, x: str, y: str):
    return sns.lineplot(data=df, x=x, y=y, errorbar=None)


def line_with_band(df: pd.DataFrame, x: str, y: str):
    return sns.lineplot(data=df, x=x, y=y, errorbar="sd")
