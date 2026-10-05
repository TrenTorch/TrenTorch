import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def histogram_axes(df: pd.DataFrame, column: str, bins: int, stat: str):
    """Histogram of `column`, `bins` bins, statistic `stat`. Returns the Axes."""
    # TODO: One seaborn histogram call.
    pass


def kde_axes(df: pd.DataFrame, column: str):
    """One kernel density curve of `column`. Returns the Axes."""
    # TODO: One seaborn density call.
    pass


def kde_by_group(df: pd.DataFrame, column: str, group: str, order: list):
    """
    One density curve per value of `group` (colours in `order`), each normalised
    on its own. Returns the Axes.
    """
    # TODO: Split by group with separate normalisation.
    pass


def ecdf_axes(df: pd.DataFrame, column: str):
    """Empirical CDF of `column`. Returns the Axes."""
    # TODO: One seaborn ECDF call.
    pass
