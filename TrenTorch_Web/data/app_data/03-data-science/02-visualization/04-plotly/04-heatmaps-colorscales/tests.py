"""
pytest tests.py
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from _load import load_solution

_module = load_solution(__file__)
heatmap_figure = _module.heatmap_figure
correlation_heatmap = _module.correlation_heatmap
annotate_strong_cells = _module.annotate_strong_cells

Z = [[1.0, 0.2, -0.9], [0.2, 1.0, 0.5], [-0.9, 0.5, 1.0]]
X = ["a", "b", "c"]
Y = ["r1", "r2", "r3"]


def _frame():
    rng = np.random.default_rng(0)
    a = rng.normal(size=100)
    return pd.DataFrame({"a": a, "b": a * 2 + rng.normal(size=100) * 0.3, "c": rng.normal(size=100), "label": ["u", "v"] * 50})


# ---- 1-7: heatmap_figure ----


def test_1_one_heatmap_trace_with_the_matrix():
    fig = heatmap_figure(Z, X, Y, "T", -1, 1, "Viridis")
    assert isinstance(fig, go.Figure) and len(fig.data) == 1
    assert fig.data[0].type == "heatmap"
    assert np.asarray(fig.data[0].z).tolist() == Z


def test_2_labels_on_both_axes():
    trace = heatmap_figure(Z, X, Y, "T", -1, 1, "Viridis").data[0]
    assert list(trace.x) == X and list(trace.y) == Y


def test_3_the_colour_range_is_pinned():
    trace = heatmap_figure(Z, X, Y, "T", -2.5, 3.5, "Viridis").data[0]
    assert trace.zmin == -2.5 and trace.zmax == 3.5


def test_4_the_colour_scale_is_the_requested_one():
    sequential = heatmap_figure(Z, X, Y, "T", -1, 1, "Viridis").data[0].colorscale
    diverging = heatmap_figure(Z, X, Y, "T", -1, 1, "RdBu").data[0].colorscale
    assert sequential != diverging
    assert sequential[0][1].lower() == "#440154"


def test_5_the_colourbar_is_titled_value():
    assert heatmap_figure(Z, X, Y, "T", -1, 1, "Viridis").data[0].colorbar.title.text == "value"


def test_6_layout_title():
    assert heatmap_figure(Z, X, Y, "My matrix", 0, 1, "Blues").layout.title.text == "My matrix"


def test_7_accepts_numpy_matrices():
    fig = heatmap_figure(np.array(Z), np.array(X), np.array(Y), "T", -1, 1, "Viridis")
    assert np.asarray(fig.data[0].z).shape == (3, 3)


# ---- 8-12: correlation_heatmap ----


def test_8_labels_are_the_numeric_columns():
    trace = correlation_heatmap(_frame()).data[0]
    assert list(trace.x) == ["a", "b", "c"] and list(trace.y) == ["a", "b", "c"]


def test_9_cells_hold_the_pearson_correlations():
    df = _frame()
    z = np.asarray(correlation_heatmap(df).data[0].z, dtype=float)
    assert z == pytest.approx(df[["a", "b", "c"]].corr().to_numpy())


def test_10_the_scale_is_diverging_symmetric_and_centred_on_zero():
    trace = correlation_heatmap(_frame()).data[0]
    assert (trace.zmin, trace.zmax, trace.zmid) == (-1, 1, 0)
    assert trace.colorscale == heatmap_figure(Z, X, Y, "T", -1, 1, "RdBu").data[0].colorscale


def test_11_cells_show_their_value_with_two_decimals():
    assert correlation_heatmap(_frame()).data[0].texttemplate == "%{z:.2f}"


def test_12_the_diagonal_is_one_and_text_columns_are_left_out():
    z = np.asarray(correlation_heatmap(_frame()).data[0].z, dtype=float)
    assert z.shape == (3, 3)
    assert np.allclose(np.diag(z), 1.0)


# ---- 13-17: annotate_strong_cells ----


def test_13_returns_the_number_of_cells_at_or_above_the_threshold():
    fig = heatmap_figure(Z, X, Y, "T", -1, 1, "RdBu")
    assert annotate_strong_cells(fig, Z, X, Y, 0.9) == 5  # three 1.0s and two -0.9s


def test_14_the_count_is_an_int_and_equals_the_number_of_annotations():
    fig = heatmap_figure(Z, X, Y, "T", -1, 1, "RdBu")
    n = annotate_strong_cells(fig, Z, X, Y, 0.5)
    assert type(n) is int
    assert n == len(fig.layout.annotations) == 7


def test_15_each_annotation_sits_on_its_cell_with_the_value_as_text():
    fig = heatmap_figure(Z, X, Y, "T", -1, 1, "RdBu")
    annotate_strong_cells(fig, Z, X, Y, 0.9)
    found = {(a.x, a.y): a.text for a in fig.layout.annotations}
    assert found[("c", "r1")] == "-0.90"
    assert found[("a", "r1")] == "1.00"
    assert ("b", "r1") not in found


def test_16_annotations_have_no_arrow():
    fig = heatmap_figure(Z, X, Y, "T", -1, 1, "RdBu")
    annotate_strong_cells(fig, Z, X, Y, 0.9)
    assert all(a.showarrow is False for a in fig.layout.annotations)


def test_17_a_threshold_above_every_value_adds_nothing():
    fig = heatmap_figure(Z, X, Y, "T", -1, 1, "RdBu")
    assert annotate_strong_cells(fig, Z, X, Y, 5.0) == 0
    assert len(fig.layout.annotations) == 0
