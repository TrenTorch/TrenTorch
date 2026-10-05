import matplotlib.pyplot as plt
import numpy as np


def draw_histogram(data, bins: int):
    fig, ax = plt.subplots()
    counts, edges, _ = ax.hist(data, bins=bins)
    return fig, ax, counts, edges


def density_histogram(data, bins: int):
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins, density=True)
    ax.set_ylabel("density")
    return fig, ax


def overlay_histograms(a, b, bins: int, labels):
    edges = np.histogram_bin_edges(np.concatenate([np.asarray(a, float), np.asarray(b, float)]), bins=bins)
    fig, ax = plt.subplots()
    ax.hist(a, bins=edges, alpha=0.5, label=labels[0])
    ax.hist(b, bins=edges, alpha=0.5, label=labels[1])
    ax.legend()
    return fig, ax, edges
