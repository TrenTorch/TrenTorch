import matplotlib.pyplot as plt
import numpy as np


def annotate_max(ax, x, y):
    y = np.asarray(y, dtype=float)
    i = int(np.argmax(y))
    return ax.annotate(
        f"max = {y[i]:g}",
        xy=(x[i], y[i]),
        xytext=(0, 20),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->"),
    )


def add_threshold(ax, value: float, label: str):
    line = ax.axhline(value, color="gray", linestyle="--", label=label)
    ax.legend()
    return line


def shade_region(ax, x0: float, x1: float, label: str):
    return ax.axvspan(x0, x1, color="orange", alpha=0.2, label=label)


def legend_below(ax, title: str):
    return ax.legend(title=title, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
