import matplotlib.pyplot as plt
import numpy as np


def draw_histogram(data, bins: int):
    """
    Histogram of `data` with `bins` bars on a new Axes. Returns
    (fig, ax, counts, edges), the arrays that `ax.hist` returned.
    """
    # TODO: Draw it and return what hist computed.
    pass


def density_histogram(data, bins: int):
    """
    Histogram whose bars have total area 1 (density); y label "density".
    Returns (fig, ax).
    """
    # TODO: Ask hist for a density.
    pass


def overlay_histograms(a, b, bins: int, labels):
    """
    Both samples on one Axes with the SAME edges, taken from the combined data
    (np.histogram_bin_edges); alpha 0.5; labels = (label_a, label_b); legend.
    Returns (fig, ax, edges).
    """
    # TODO: Compute shared edges, then draw both.
    pass
