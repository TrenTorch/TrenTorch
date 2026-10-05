"""
pytest tests.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
histograms_by_group = _module.histograms_by_group
bars_by_group = _module.bars_by_group
pair_scatter = _module.pair_scatter


def _fresh():
    plt.close("all")


def _frame():
    rng = np.random.default_rng(0)
    n = 120
    return pd.DataFrame(
        {
            "g": np.tile(["north", "south", "east"], 40),
            "kind": np.tile(["p", "q", "r", "s"], 30),
            "v": rng.normal(size=n),
            "w": rng.normal(size=n),
            "z": rng.normal(size=n),
        }
    )


# ---- 1-6: histograms_by_group ----


def test_1_returns_a_facet_grid_with_one_panel_per_group():
    _fresh()
    g = histograms_by_group(_frame(), "v", "g", ["north", "south", "east"], 6)
    assert type(g).__name__ == "FacetGrid"
    assert g.axes.shape == (1, 3)


def test_2_panels_follow_the_requested_order_and_are_titled():
    _fresh()
    g = histograms_by_group(_frame(), "v", "g", ["east", "north", "south"], 6)
    assert [a.get_title() for a in g.axes.flat] == ["g = east", "g = north", "g = south"]


def test_3_each_panel_has_the_requested_number_of_bars():
    _fresh()
    g = histograms_by_group(_frame(), "v", "g", ["north", "south", "east"], 7)
    assert [len(a.patches) for a in g.axes.flat] == [7, 7, 7]


def test_4_each_panel_counts_only_its_own_rows():
    _fresh()
    df = _frame()
    g = histograms_by_group(df, "v", "g", ["north", "south", "east"], 6)
    for ax, group in zip(g.axes.flat, ["north", "south", "east"]):
        assert sum(p.get_height() for p in ax.patches) == (df["g"] == group).sum()


def test_5_panels_use_the_same_bin_edges_across_the_whole_data_range():
    _fresh()
    df = _frame()
    g = histograms_by_group(df, "v", "g", ["north", "south", "east"], 6)
    edges = np.histogram_bin_edges(df["v"], bins=6)
    for ax in g.axes.flat:
        assert [p.get_x() for p in ax.patches] == pytest.approx(edges[:-1].tolist())


def test_6_the_panels_share_their_axes():
    _fresh()
    g = histograms_by_group(_frame(), "v", "g", ["north", "south", "east"], 6)
    axes = list(g.axes.flat)
    assert axes[0].get_shared_x_axes().joined(axes[0], axes[1])
    assert axes[0].get_shared_y_axes().joined(axes[0], axes[2])


# ---- 7-12: bars_by_group ----


def test_7_returns_a_facet_grid_with_the_groups_in_order():
    _fresh()
    g = bars_by_group(_frame(), "kind", "v", "g", ["south", "east", "north"])
    assert type(g).__name__ == "FacetGrid"
    assert [a.get_title() for a in g.axes.flat] == ["g = south", "g = east", "g = north"]


def test_8_each_panel_has_one_bar_per_category():
    _fresh()
    g = bars_by_group(_frame(), "kind", "v", "g", ["north", "south", "east"])
    assert [len(a.patches) for a in g.axes.flat] == [4, 4, 4]


def test_9_bar_heights_are_the_group_means():
    _fresh()
    df = _frame()
    g = bars_by_group(df, "kind", "v", "g", ["north", "south", "east"])
    for ax, group in zip(g.axes.flat, ["north", "south", "east"]):
        means = df[df["g"] == group].groupby("kind")["v"].mean()
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert [p.get_height() for p in ax.patches] == pytest.approx([means[k] for k in labels])


def test_10_categories_appear_in_order_of_first_occurrence():
    _fresh()
    g = bars_by_group(_frame(), "kind", "v", "g", ["north", "south", "east"])
    assert [t.get_text() for t in g.axes.flat[0].get_xticklabels()] == ["p", "q", "r", "s"]


def test_11_there_are_no_error_bars():
    _fresh()
    g = bars_by_group(_frame(), "kind", "v", "g", ["north", "south", "east"])
    assert all(len(a.lines) == 0 for a in g.axes.flat)


def test_12_axis_labels_name_the_columns():
    _fresh()
    g = bars_by_group(_frame(), "kind", "v", "g", ["north", "south", "east"])
    assert g.axes.flat[0].get_xlabel() == "kind" and g.axes.flat[0].get_ylabel() == "v"


# ---- 13-17: pair_scatter ----


def test_13_one_row_and_column_per_variable():
    _fresh()
    grid = pair_scatter(_frame(), ["v", "w", "z"])
    assert type(grid).__name__ == "PairGrid"
    assert grid.axes.shape == (3, 3)


def test_14_only_the_requested_variables_are_used_in_order():
    _fresh()
    grid = pair_scatter(_frame(), ["z", "v"])
    assert grid.axes.shape == (2, 2)
    assert [a.get_xlabel() for a in grid.axes[-1]] == ["z", "v"]
    assert [grid.axes[i, 0].get_ylabel() for i in range(2)] == ["z", "v"]


def test_15_off_diagonal_panels_scatter_every_row():
    _fresh()
    df = _frame()
    grid = pair_scatter(df, ["v", "w"])
    offsets = np.asarray(grid.axes[1, 0].collections[0].get_offsets())
    assert offsets.shape == (len(df), 2)
    assert offsets[:, 0].tolist() == pytest.approx(df["v"].tolist())
    assert offsets[:, 1].tolist() == pytest.approx(df["w"].tolist())


def test_16_the_transposed_panel_swaps_the_axes():
    _fresh()
    df = _frame()
    grid = pair_scatter(df, ["v", "w"])
    offsets = np.asarray(grid.axes[0, 1].collections[0].get_offsets())
    assert offsets[:, 0].tolist() == pytest.approx(df["w"].tolist())
    assert offsets[:, 1].tolist() == pytest.approx(df["v"].tolist())


def test_17_every_panel_belongs_to_the_grids_figure():
    _fresh()
    grid = pair_scatter(_frame(), ["v", "w", "z"])
    assert all(ax in grid.figure.axes for ax in grid.axes.flat)
    assert len(set(map(id, grid.axes.flat))) == 9
