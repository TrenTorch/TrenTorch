"""
pytest tests.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
draw_histogram = _module.draw_histogram
density_histogram = _module.density_histogram
overlay_histograms = _module.overlay_histograms


def _fresh():
    plt.close("all")


def _data(seed=0, n=200, loc=0.0, scale=1.0):
    return np.random.default_rng(seed).normal(loc, scale, n)


# ---- 1-6: draw_histogram ----


def test_1_one_bar_per_bin():
    _fresh()
    _, ax, counts, edges = draw_histogram(_data(), 12)
    assert len(ax.patches) == 12
    assert len(counts) == 12 and len(edges) == 13


def test_2_counts_and_edges_match_numpy():
    _fresh()
    x = _data(1)
    _, _, counts, edges = draw_histogram(x, 9)
    ref_counts, ref_edges = np.histogram(x, bins=9)
    assert counts.tolist() == ref_counts.tolist()
    assert edges.tolist() == pytest.approx(ref_edges.tolist())


def test_3_the_bars_on_the_axes_have_the_counts_as_heights():
    _fresh()
    x = _data(2)
    _, ax, counts, _ = draw_histogram(x, 7)
    assert [p.get_height() for p in ax.patches] == counts.tolist()


def test_4_bar_positions_follow_the_edges():
    _fresh()
    x = _data(3)
    _, ax, _, edges = draw_histogram(x, 6)
    assert [p.get_x() for p in ax.patches] == pytest.approx(edges[:-1].tolist())
    assert [p.get_width() for p in ax.patches] == pytest.approx(np.diff(edges).tolist())


def test_5_counts_add_up_to_the_number_of_values():
    _fresh()
    x = _data(4, n=137)
    _, _, counts, _ = draw_histogram(x, 10)
    assert counts.sum() == 137


def test_6_a_figure_with_one_axes_is_returned():
    _fresh()
    fig, ax, _, _ = draw_histogram([1, 2, 2, 3, 3, 3], 3)
    assert fig.axes == [ax]


# ---- 7-11: density_histogram ----


def test_7_the_bars_have_total_area_one():
    _fresh()
    _, ax = density_histogram(_data(5), 15)
    area = sum(p.get_height() * p.get_width() for p in ax.patches)
    assert area == pytest.approx(1.0)


def test_8_heights_match_numpy_density():
    _fresh()
    x = _data(6)
    _, ax = density_histogram(x, 8)
    ref, _ = np.histogram(x, bins=8, density=True)
    assert [p.get_height() for p in ax.patches] == pytest.approx(ref.tolist())


def test_9_the_y_label_is_density():
    _fresh()
    _, ax = density_histogram(_data(7), 5)
    assert ax.get_ylabel() == "density"


def test_10_the_number_of_bars_is_the_bins_argument():
    _fresh()
    _, ax = density_histogram(_data(8), 11)
    assert len(ax.patches) == 11


def test_11_works_for_integer_data():
    _fresh()
    _, ax = density_histogram([1, 1, 2, 3, 3, 3, 4], 4)
    assert sum(p.get_height() * p.get_width() for p in ax.patches) == pytest.approx(1.0)


# ---- 12-17: overlay_histograms ----


def test_12_returns_the_shared_edges_from_the_combined_data():
    _fresh()
    a, b = _data(1), _data(2, loc=2.0)
    _, _, edges = overlay_histograms(a, b, 10, ("a", "b"))
    ref = np.histogram_bin_edges(np.concatenate([a, b]), bins=10)
    assert edges.tolist() == pytest.approx(ref.tolist())


def test_13_both_samples_use_exactly_those_bins():
    _fresh()
    a, b = _data(1), _data(2, loc=2.0)
    _, ax, edges = overlay_histograms(a, b, 10, ("a", "b"))
    assert len(ax.patches) == 20
    first, second = ax.patches[:10], ax.patches[10:]
    assert [p.get_x() for p in first] == pytest.approx(edges[:-1].tolist())
    assert [p.get_x() for p in second] == pytest.approx(edges[:-1].tolist())


def test_14_each_sample_has_its_own_counts():
    _fresh()
    a, b = _data(1), _data(2, loc=2.0)
    _, ax, edges = overlay_histograms(a, b, 10, ("a", "b"))
    assert [p.get_height() for p in ax.patches[:10]] == np.histogram(a, bins=edges)[0].tolist()
    assert [p.get_height() for p in ax.patches[10:]] == np.histogram(b, bins=edges)[0].tolist()


def test_15_both_are_semi_transparent():
    _fresh()
    _, ax, _ = overlay_histograms(_data(1), _data(2), 6, ("a", "b"))
    assert all(p.get_alpha() == 0.5 for p in ax.patches)


def test_16_legend_shows_the_labels_in_order():
    _fresh()
    _, ax, _ = overlay_histograms(_data(1), _data(2), 6, ("control", "treated"))
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["control", "treated"]


def test_17_everything_is_on_a_single_axes():
    _fresh()
    fig, ax, _ = overlay_histograms(_data(1), _data(2), 6, ("a", "b"))
    assert fig.axes == [ax]
