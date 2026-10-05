import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def ranked_order(df: pd.DataFrame, cat: str, value: str) -> list:
    """Categories of `cat` by mean of `value`, largest first; ties by name ascending."""
    # TODO: Average per category, then sort with a tie-break.
    pass


def mean_bars(df: pd.DataFrame, cat: str, value: str, order: list):
    """One bar per category in `order`: the mean of `value`, no error bars. Returns the Axes."""
    # TODO: Draw the means.
    pass


def count_bars(df: pd.DataFrame, cat: str, hue: str, order: list, hue_order: list):
    """Bars counting rows per (category, hue) with the given orders. Returns the Axes."""
    # TODO: Draw the counts, split by hue.
    pass


def horizontal_means(df: pd.DataFrame, cat: str, value: str, order: list):
    """Horizontal bars of the mean of `value` per category in `order`, no error bars. Returns the Axes."""
    # TODO: Same as mean_bars but with the roles of the axes swapped.
    pass
