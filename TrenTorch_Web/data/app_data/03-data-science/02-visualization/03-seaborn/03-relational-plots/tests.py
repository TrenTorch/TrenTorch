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
scatter_by_group = _module.scatter_by_group
mean_line = _module.mean_line
line_with_band = _module.line_with_band


def _fresh():
    plt.close("all")


def _points():
    rng = np.random.default_rng(0)
    n = 60
    return pd.DataFrame({"x": rng.normal(size=n), "y": rng.normal(size=n), "kind": np.tile(["cat", "dog", "owl"], 20)})


def _repeats():
    return pd.DataFrame({"t": [1, 1, 1, 2, 2, 2, 3, 3, 3], "v": [1.0, 2.0, 3.0, 10.0, 20.0, 30.0, 5.0, 5.0, 8.0]})


# ---- 1-7: scatter_by_group ----


def test_1_one_collection_with_every_point():
    _fresh()
    df = _points()
    ax = scatter_by_group(df, "x", "y", "kind", ["cat", "dog", "owl"])
    assert len(ax.collections) == 1
    assert ax.collections[0].get_offsets().shape == (60, 2)


def test_2_points_are_at_the_data_values():
    _fresh()
    df = _points()
    ax = scatter_by_group(df, "x", "y", "kind", ["cat", "dog", "owl"])
    offsets = np.asarray(ax.collections[0].get_offsets())
    assert offsets[:, 0].tolist() == pytest.approx(df["x"].tolist())
    assert offsets[:, 1].tolist() == pytest.approx(df["y"].tolist())


def test_3_legend_entries_follow_hue_order():
    _fresh()
    ax = scatter_by_group(_points(), "x", "y", "kind", ["owl", "cat", "dog"])
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["owl", "cat", "dog"]


def test_4_legend_is_titled_by_the_hue_column():
    _fresh()
    ax = scatter_by_group(_points(), "x", "y", "kind", ["cat", "dog", "owl"])
    assert ax.get_legend().get_title().get_text() == "kind"


def test_5_each_group_has_one_colour_and_the_groups_differ():
    _fresh()
    df = _points()
    ax = scatter_by_group(df, "x", "y", "kind", ["cat", "dog", "owl"])
    colours = [tuple(np.round(c, 3)) for c in ax.collections[0].get_facecolors()]
    by_group = {}
    for group, colour in zip(df["kind"], colours):
        by_group.setdefault(group, set()).add(colour)
    assert all(len(v) == 1 for v in by_group.values())
    assert len({next(iter(v)) for v in by_group.values()}) == 3


def test_6_hue_order_assigns_the_colours_in_that_order():
    _fresh()
    df = _points()
    ax1 = scatter_by_group(df, "x", "y", "kind", ["cat", "dog", "owl"])
    c1 = {g: tuple(np.round(c, 3)) for g, c in zip(df["kind"], ax1.collections[0].get_facecolors())}
    _fresh()
    ax2 = scatter_by_group(df, "x", "y", "kind", ["owl", "dog", "cat"])
    c2 = {g: tuple(np.round(c, 3)) for g, c in zip(df["kind"], ax2.collections[0].get_facecolors())}
    assert c1["cat"] == c2["owl"] and c1["owl"] == c2["cat"]


def test_7_axis_labels_are_the_column_names():
    _fresh()
    ax = scatter_by_group(_points(), "x", "y", "kind", ["cat", "dog", "owl"])
    assert ax.get_xlabel() == "x" and ax.get_ylabel() == "y"


# ---- 8-11: mean_line ----


def test_8_one_line_and_no_band():
    _fresh()
    ax = mean_line(_repeats(), "t", "v")
    assert len(ax.lines) == 1
    assert len(ax.collections) == 0


def test_9_the_line_is_the_mean_at_each_x():
    _fresh()
    ax = mean_line(_repeats(), "t", "v")
    line = ax.lines[0]
    assert line.get_xdata().tolist() == [1, 2, 3]
    assert line.get_ydata().tolist() == pytest.approx([2.0, 20.0, 6.0])


def test_10_x_values_are_ascending_even_if_rows_are_shuffled():
    _fresh()
    df = _repeats().sample(frac=1.0, random_state=1)
    ax = mean_line(df, "t", "v")
    assert ax.lines[0].get_xdata().tolist() == [1, 2, 3]
    assert ax.lines[0].get_ydata().tolist() == pytest.approx([2.0, 20.0, 6.0])


def test_11_one_row_per_x_gives_the_raw_values():
    _fresh()
    df = pd.DataFrame({"t": [3, 1, 2], "v": [30.0, 10.0, 20.0]})
    ax = mean_line(df, "t", "v")
    assert ax.lines[0].get_ydata().tolist() == [10.0, 20.0, 30.0]


# ---- 12-15: line_with_band ----


def test_12_one_line_and_one_band():
    _fresh()
    ax = line_with_band(_repeats(), "t", "v")
    assert len(ax.lines) == 1
    assert len(ax.collections) == 1


def test_13_the_line_is_still_the_mean():
    _fresh()
    ax = line_with_band(_repeats(), "t", "v")
    assert ax.lines[0].get_ydata().tolist() == pytest.approx([2.0, 20.0, 6.0])


def test_14_the_band_spans_mean_plus_and_minus_one_sample_std():
    _fresh()
    df = _repeats()
    ax = line_with_band(df, "t", "v")
    vertices = np.asarray(ax.collections[0].get_paths()[0].vertices)
    for t, group in df.groupby("t")["v"]:
        mean, sd = group.mean(), group.std(ddof=1)
        ys = vertices[np.isclose(vertices[:, 0], t), 1]
        assert ys.min() == pytest.approx(mean - sd)
        assert ys.max() == pytest.approx(mean + sd)


def test_15_a_noisier_x_gets_a_wider_band():
    _fresh()
    ax = line_with_band(_repeats(), "t", "v")
    vertices = np.asarray(ax.collections[0].get_paths()[0].vertices)
    width = {t: np.ptp(vertices[np.isclose(vertices[:, 0], t), 1]) for t in (1, 2, 3)}
    assert width[2] > width[1] > width[3] * 0.0
    assert width[2] > width[3]
