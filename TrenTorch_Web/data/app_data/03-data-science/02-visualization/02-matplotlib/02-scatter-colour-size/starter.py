import matplotlib.pyplot as plt
import numpy as np


def scatter_chart(x, y, sizes, values, label: str):
    """
    New figure with one scatter of (x, y): marker areas `sizes`, coloured by
    `values` with the "viridis" colormap, plus a colourbar labelled `label`.
    Returns (fig, ax, points) where points is the scatter collection.
    """
    # TODO: Draw the scatter and attach a colourbar.
    pass


def fit_line(ax, x, y):
    """
    Draw the least-squares line as one red segment from min(x) to max(x),
    label "fit". Returns (slope, intercept) as Python floats.
    """
    # TODO: Fit, then draw the segment.
    pass


def highlight_outliers(ax, x, y, k: float) -> int:
    """
    Second scatter (red, area 80) of the points with |y - mean(y)| > k * std(y)
    (population std). Returns how many; draws nothing if there are none.
    """
    # TODO: Find the points far from the mean and draw them.
    pass
