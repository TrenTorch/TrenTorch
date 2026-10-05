import matplotlib.pyplot as plt
import numpy as np


def line_chart(x, y, title: str, xlabel: str, ylabel: str):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    return fig, ax


def add_line(ax, x, y, label: str, color: str):
    (line,) = ax.plot(x, y, label=label, color=color)
    ax.legend()
    return line


def line_data(ax) -> list:
    return [(np.asarray(line.get_xdata()).tolist(), np.asarray(line.get_ydata()).tolist()) for line in ax.lines]


def style_line(line, color: str, linestyle: str, linewidth: float, marker: str):
    line.set_color(color)
    line.set_linestyle(linestyle)
    line.set_linewidth(linewidth)
    line.set_marker(marker)
    return line
