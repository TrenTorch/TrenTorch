import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def ranked_order(df: pd.DataFrame, cat: str, value: str) -> list:
    means = df.groupby(cat)[value].mean()
    ordered = sorted(means.items(), key=lambda item: (-item[1], item[0]))
    return [name for name, _ in ordered]


def mean_bars(df: pd.DataFrame, cat: str, value: str, order: list):
    return sns.barplot(data=df, x=cat, y=value, order=order, estimator="mean", errorbar=None)


def count_bars(df: pd.DataFrame, cat: str, hue: str, order: list, hue_order: list):
    return sns.countplot(data=df, x=cat, hue=hue, order=order, hue_order=hue_order)


def horizontal_means(df: pd.DataFrame, cat: str, value: str, order: list):
    return sns.barplot(data=df, x=value, y=cat, order=order, estimator="mean", errorbar=None, orient="h")
