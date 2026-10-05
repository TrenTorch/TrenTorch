import math

import matplotlib.pyplot as plt
import numpy as np


def small_multiples(series: dict, ncols: int):
    """
    One panel per entry of `series` ({title: (x, y)}), row-major in a grid of
    ceil(n / ncols) rows and `ncols` columns, sharing both axes. Unused panels
    are hidden. Returns (fig, axes) with axes a 2D array.
    """
    # TODO: Make the shared grid, draw each panel, hide the extras.
    pass


def twin_axis_chart(x, y_left, y_right, left_label: str, right_label: str):
    """
    y_left in "tab:blue" on the left axes, y_right in "tab:red" on a twin axes
    sharing x; each y label coloured like its line. Returns (fig, ax_left, ax_right).
    """
    # TODO: Plot on two y axes that share x.
    pass


def set_limits_and_ticks(ax, xlim, ylim, xticks, xticklabels, logy: bool) -> None:
    """Set limits, x ticks with their text, and a log y scale if `logy`."""
    # TODO: Apply the limits, ticks and scale to `ax`.
    pass
