import pandas as pd
import plotly.express as px


def scatter_by_group(df: pd.DataFrame, x: str, y: str, group: str, order: list):
    """Scatter with one trace per value of `group`, traces in `order`. Returns the figure."""
    # TODO: Map the group column to colour and fix the order.
    pass


def total_bars(df: pd.DataFrame, cat: str, value: str):
    """One bar per category: the sum of `value`, largest first, ties by name. Returns the figure."""
    # TODO: Aggregate with pandas, then draw.
    pass


def histogram_figure(df: pd.DataFrame, column: str, bins: int):
    """Histogram of `column` requesting `bins` bins. Returns the figure."""
    # TODO: One Express histogram call.
    pass


def lines_by_group(df: pd.DataFrame, x: str, y: str, group: str):
    """
    One line per group (groups in order of first appearance), each sorted by
    x ascending. Returns the figure.
    """
    # TODO: Sort, then draw one line per group.
    pass
