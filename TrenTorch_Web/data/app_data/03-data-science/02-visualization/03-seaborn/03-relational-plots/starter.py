import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def scatter_by_group(df: pd.DataFrame, x: str, y: str, hue: str, hue_order: list):
    """One point per row, coloured by `hue`, legend in `hue_order`. Returns the Axes."""
    # TODO: Scatter plot with a hue.
    pass


def mean_line(df: pd.DataFrame, x: str, y: str):
    """One line of the mean of y at each distinct x (ascending), no band. Returns the Axes."""
    # TODO: Line plot without an uncertainty band.
    pass


def line_with_band(df: pd.DataFrame, x: str, y: str):
    """The mean line plus a band of +/- one sample standard deviation. Returns the Axes."""
    # TODO: Line plot with a standard-deviation band.
    pass
