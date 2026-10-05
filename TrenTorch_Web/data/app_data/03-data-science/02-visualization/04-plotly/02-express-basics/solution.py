import pandas as pd
import plotly.express as px


def scatter_by_group(df: pd.DataFrame, x: str, y: str, group: str, order: list):
    return px.scatter(df, x=x, y=y, color=group, category_orders={group: list(order)})


def total_bars(df: pd.DataFrame, cat: str, value: str):
    totals = df.groupby(cat, as_index=False)[value].sum()
    totals = totals.sort_values([value, cat], ascending=[False, True], kind="mergesort")
    return px.bar(totals, x=cat, y=value)


def histogram_figure(df: pd.DataFrame, column: str, bins: int):
    return px.histogram(df, x=column, nbins=bins)


def lines_by_group(df: pd.DataFrame, x: str, y: str, group: str):
    first_seen = list(dict.fromkeys(df[group]))
    ordered = df.sort_values(x, kind="mergesort")
    return px.line(ordered, x=x, y=y, color=group, category_orders={group: first_seen})
