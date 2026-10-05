import math

import matplotlib.pyplot as plt
import numpy as np


def small_multiples(series: dict, ncols: int):
    n = len(series)
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(nrows, ncols, sharex=True, sharey=True, squeeze=False)
    flat = axes.flatten()
    for ax, (title, (x, y)) in zip(flat, series.items()):
        ax.plot(x, y)
        ax.set_title(title)
    for ax in flat[n:]:
        ax.set_visible(False)
    return fig, axes


def twin_axis_chart(x, y_left, y_right, left_label: str, right_label: str):
    fig, ax_left = plt.subplots()
    ax_left.plot(x, y_left, color="tab:blue")
    ax_left.set_ylabel(left_label, color="tab:blue")
    ax_right = ax_left.twinx()
    ax_right.plot(x, y_right, color="tab:red")
    ax_right.set_ylabel(right_label, color="tab:red")
    return fig, ax_left, ax_right


def set_limits_and_ticks(ax, xlim, ylim, xticks, xticklabels, logy: bool) -> None:
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(list(xticks))
    ax.set_xticklabels(list(xticklabels))
    ax.set_yscale("log" if logy else "linear")
