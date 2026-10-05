import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def histograms_by_group(df: pd.DataFrame, value: str, col: str, col_order: list, bins: int):
    """FacetGrid: one histogram panel of `value` per group in `col_order`. Returns the grid."""
    # TODO: Facet a histogram by group.
    pass


def bars_by_group(df: pd.DataFrame, x: str, y: str, col: str, col_order: list):
    """FacetGrid: one panel per group, bars of the mean of y per x, no error bars. Returns the grid."""
    # TODO: Facet a bar chart by group.
    pass


def pair_scatter(df: pd.DataFrame, variables: list):
    """PairGrid of exactly `variables` (rows and columns, in that order). Returns the grid."""
    # TODO: Pairwise plots of the given columns.
    pass
