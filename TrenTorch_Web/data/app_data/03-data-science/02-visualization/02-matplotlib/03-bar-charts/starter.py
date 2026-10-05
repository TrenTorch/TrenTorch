import matplotlib.pyplot as plt
import numpy as np


def bar_chart(labels: list, values: list):
    """
    Bars centred at 0..n-1 (width 0.8), ticks at 0..n-1 labelled with `labels`,
    y axis starting at 0. Returns (fig, ax).
    """
    # TODO: Draw the bars at numeric positions, then label the ticks.
    pass


def grouped_bars(labels: list, series: dict):
    """
    k series side by side per category: width 0.8/k, series j offset by
    (j - (k - 1) / 2) * width. Ticks 0..n-1 with labels; legend of series names.
    Returns (fig, ax).
    """
    # TODO: Offset each series within its group.
    pass


def stacked_bars(labels: list, series: dict):
    """
    Bars of width 0.6 at 0..n-1; each series starts where the previous ones
    end. Ticks 0..n-1 with labels; legend of series names. Returns (fig, ax).
    """
    # TODO: Track the running bottom.
    pass


def annotate_bars(ax) -> list:
    """
    Write each bar's height (f"{height:g}") centred above its top, and return
    those strings in ax.patches order.
    """
    # TODO: Add a text label to every patch.
    pass
