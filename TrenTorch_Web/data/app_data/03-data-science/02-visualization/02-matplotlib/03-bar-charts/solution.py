import matplotlib.pyplot as plt
import numpy as np


def _ticks(ax, labels):
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)


def bar_chart(labels: list, values: list):
    fig, ax = plt.subplots()
    ax.bar(range(len(values)), values, width=0.8)
    _ticks(ax, labels)
    ax.set_ylim(bottom=0)
    return fig, ax


def grouped_bars(labels: list, series: dict):
    fig, ax = plt.subplots()
    k = len(series)
    width = 0.8 / k
    positions = np.arange(len(labels))
    for j, (name, values) in enumerate(series.items()):
        offset = (j - (k - 1) / 2) * width
        ax.bar(positions + offset, values, width=width, label=name)
    _ticks(ax, labels)
    ax.legend()
    return fig, ax


def stacked_bars(labels: list, series: dict):
    fig, ax = plt.subplots()
    positions = np.arange(len(labels))
    bottom = np.zeros(len(labels))
    for name, values in series.items():
        ax.bar(positions, values, width=0.6, bottom=bottom, label=name)
        bottom = bottom + np.asarray(values, dtype=float)
    _ticks(ax, labels)
    ax.legend()
    return fig, ax


def annotate_bars(ax) -> list:
    texts = []
    for patch in ax.patches:
        text = f"{patch.get_height():g}"
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_y() + patch.get_height(), text, ha="center", va="bottom")
        texts.append(text)
    return texts
