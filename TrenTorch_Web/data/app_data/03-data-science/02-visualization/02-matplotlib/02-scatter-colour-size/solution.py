import matplotlib.pyplot as plt
import numpy as np


def scatter_chart(x, y, sizes, values, label: str):
    fig, ax = plt.subplots()
    points = ax.scatter(x, y, s=sizes, c=values, cmap="viridis")
    fig.colorbar(points, ax=ax, label=label)
    return fig, ax, points


def fit_line(ax, x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    ends = np.array([x.min(), x.max()])
    ax.plot(ends, slope * ends + intercept, color="red", label="fit")
    return float(slope), float(intercept)


def highlight_outliers(ax, x, y, k: float) -> int:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.abs(y - y.mean()) > k * y.std()
    count = int(mask.sum())
    if count:
        ax.scatter(x[mask], y[mask], color="red", s=80)
    return count
