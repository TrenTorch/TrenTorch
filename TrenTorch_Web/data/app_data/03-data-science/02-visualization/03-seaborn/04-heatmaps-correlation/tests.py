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
correlation_matrix = _module.correlation_matrix
heatmap_axes = _module.heatmap_axes
upper_triangle_mask = _module.upper_triangle_mask
masked_heatmap = _module.masked_heatmap


def _fresh():
    plt.close("all")


def _frame():
    rng = np.random.default_rng(0)
    a = rng.normal(size=80)
    return pd.DataFrame(
        {
            "a": a,
            "b": 2 * a + rng.normal(size=80) * 0.5,
            "c": rng.normal(size=80),
            "label": ["u", "v"] * 40,
            "flag": [True, False] * 40,
        }
    )


def _values(ax):
    return np.ma.filled(np.ma.masked_invalid(np.asarray(ax.collections[0].get_array(), dtype=float)), np.nan)


def _is_coolwarm(mesh):
    # seaborn wraps the colormap in a new object, so compare the colours it produces.
    reference = plt.get_cmap("coolwarm")
    return all(np.allclose(mesh.get_cmap()(v), reference(v), atol=0.01) for v in (0.0, 0.25, 0.5, 0.75, 1.0))


# ---- 1-4: correlation_matrix ----


def test_1_only_numeric_columns_appear():
    out = correlation_matrix(_frame())
    assert out.columns.tolist() == ["a", "b", "c"]
    assert out.index.tolist() == ["a", "b", "c"]


def test_2_values_match_the_pearson_definition():
    df = _frame()
    out = correlation_matrix(df)
    assert out.loc["a", "b"] == pytest.approx(np.corrcoef(df["a"], df["b"])[0, 1])
    assert out.loc["a", "c"] == pytest.approx(np.corrcoef(df["a"], df["c"])[0, 1])


def test_3_diagonal_is_one_and_the_matrix_is_symmetric():
    out = correlation_matrix(_frame())
    assert np.allclose(np.diag(out), 1.0)
    assert np.allclose(out, out.T)


def test_4_text_and_boolean_columns_are_excluded():
    out = correlation_matrix(_frame())
    assert "label" not in out.columns and "flag" not in out.columns


# ---- 5-10: heatmap_axes ----


def test_5_the_cells_hold_the_matrix_values():
    _fresh()
    corr = correlation_matrix(_frame())
    ax = heatmap_axes(corr, False)
    assert _values(ax).ravel().tolist() == pytest.approx(corr.to_numpy().ravel().tolist())


def test_6_the_colour_scale_is_pinned_from_minus_one_to_one():
    _fresh()
    ax = heatmap_axes(correlation_matrix(_frame()), False)
    assert ax.collections[0].get_clim() == (-1, 1)


def test_7_the_colour_map_is_coolwarm():
    _fresh()
    ax = heatmap_axes(correlation_matrix(_frame()), False)
    assert _is_coolwarm(ax.collections[0])


def test_8_tick_labels_are_the_column_names():
    _fresh()
    ax = heatmap_axes(correlation_matrix(_frame()), False)
    assert [t.get_text() for t in ax.get_xticklabels()] == ["a", "b", "c"]
    assert [t.get_text() for t in ax.get_yticklabels()] == ["a", "b", "c"]


def test_9_annotations_show_each_value_with_two_decimals():
    _fresh()
    corr = correlation_matrix(_frame())
    ax = heatmap_axes(corr, True)
    assert [t.get_text() for t in ax.texts] == [f"{v:.2f}" for v in corr.to_numpy().ravel()]


def test_10_no_annotations_unless_asked_and_the_cells_are_square():
    _fresh()
    ax = heatmap_axes(correlation_matrix(_frame()), False)
    assert len(ax.texts) == 0
    assert ax.get_aspect() in (1.0, "equal", 1)


# ---- 11-13: upper_triangle_mask ----


def test_11_shape_and_dtype():
    mask = upper_triangle_mask(4)
    assert mask.shape == (4, 4) and mask.dtype == bool


def test_12_true_strictly_above_the_diagonal():
    mask = upper_triangle_mask(3)
    assert mask.tolist() == [[False, True, True], [False, False, True], [False, False, False]]


def test_13_counts_for_several_sizes():
    for n in (1, 2, 5, 8):
        assert int(upper_triangle_mask(n).sum()) == n * (n - 1) // 2
        assert not upper_triangle_mask(n).diagonal().any()


# ---- 14-17: masked_heatmap ----


def test_14_cells_above_the_diagonal_are_masked():
    _fresh()
    corr = correlation_matrix(_frame())
    ax = masked_heatmap(corr)
    masked = np.ma.getmaskarray(ax.collections[0].get_array()).reshape(3, 3)
    assert masked.tolist() == upper_triangle_mask(3).tolist()


def test_15_only_the_visible_cells_are_annotated():
    _fresh()
    corr = correlation_matrix(_frame())
    ax = masked_heatmap(corr)
    assert len(ax.texts) == 3 * 4 // 2


def test_16_annotations_are_the_lower_triangle_values_row_by_row():
    _fresh()
    corr = correlation_matrix(_frame())
    ax = masked_heatmap(corr)
    expected = [f"{corr.iloc[i, j]:.2f}" for i in range(3) for j in range(i + 1)]
    assert [t.get_text() for t in ax.texts] == expected


def test_17_the_colour_scale_is_still_pinned():
    _fresh()
    ax = masked_heatmap(correlation_matrix(_frame()))
    assert ax.collections[0].get_clim() == (-1, 1)
    assert _is_coolwarm(ax.collections[0])
