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
sales_dashboard = _module.sales_dashboard


def _fresh():
    plt.close("all")


def _orders():
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2024-01-05", "2024-01-20", "2024-02-02", "2024-03-03", "2024-03-30", "2024-03-31", "2024-02-14", "2024-01-09"]
            ),
            "region": ["south", "north", "north", "east", "south", "north", "east", "south"],
            "amount": [10.0, 40.0, 25.0, 5.0, 30.0, 15.0, 5.0, 20.0],
        }
    )


# ---- 1-4: the figure ----


def test_1_three_axes_in_one_row_in_order():
    _fresh()
    fig = sales_dashboard(_orders())
    assert len(fig.axes) == 3
    assert [ax.get_title() for ax in fig.axes] == ["Revenue by month", "Revenue by region", "Order amounts"]


def test_2_axes_are_side_by_side():
    _fresh()
    fig = sales_dashboard(_orders())
    tops = [round(ax.get_position().y0, 3) for ax in fig.axes]
    lefts = [ax.get_position().x0 for ax in fig.axes]
    assert len(set(tops)) == 1
    assert lefts == sorted(lefts)


def test_3_the_figure_has_an_overall_title():
    _fresh()
    fig = sales_dashboard(_orders())
    assert fig._suptitle is not None and fig._suptitle.get_text() == "Sales dashboard"


def test_4_axis_labels_on_every_panel():
    _fresh()
    fig = sales_dashboard(_orders())
    got = [(ax.get_xlabel(), ax.get_ylabel()) for ax in fig.axes]
    assert got == [("Month", "Revenue"), ("Region", "Revenue"), ("Amount", "Orders")]


# ---- 5-8: revenue by month ----


def test_5_one_line_with_one_point_per_month():
    _fresh()
    ax = sales_dashboard(_orders()).axes[0]
    assert len(ax.lines) == 1
    assert len(ax.lines[0].get_ydata()) == 3


def test_6_the_monthly_totals_are_correct_and_chronological():
    _fresh()
    ax = sales_dashboard(_orders()).axes[0]
    assert ax.lines[0].get_ydata().tolist() == [70.0, 30.0, 50.0]


def test_7_months_are_in_order_even_if_the_rows_are_not():
    _fresh()
    shuffled = _orders().sample(frac=1.0, random_state=3).reset_index(drop=True)
    ax = sales_dashboard(shuffled).axes[0]
    assert ax.lines[0].get_ydata().tolist() == [70.0, 30.0, 50.0]


def test_8_the_input_frame_is_not_changed():
    _fresh()
    df = _orders()
    before = df.copy()
    sales_dashboard(df)
    pd.testing.assert_frame_equal(df, before)


# ---- 9-13: revenue by region ----


def test_9_one_bar_per_region():
    _fresh()
    ax = sales_dashboard(_orders()).axes[1]
    assert len(ax.patches) == 3


def test_10_bars_are_ordered_largest_first_with_the_right_totals():
    _fresh()
    ax = sales_dashboard(_orders()).axes[1]
    assert [p.get_height() for p in ax.patches] == [80.0, 60.0, 10.0]


def test_11_tick_labels_name_the_regions_in_bar_order():
    _fresh()
    ax = sales_dashboard(_orders()).axes[1]
    assert [t.get_text() for t in ax.get_xticklabels()] == ["north", "south", "east"]


def test_12_bars_sit_at_integer_positions():
    _fresh()
    ax = sales_dashboard(_orders()).axes[1]
    centres = [p.get_x() + p.get_width() / 2 for p in ax.patches]
    assert centres == pytest.approx([0, 1, 2])


def test_13_ties_are_broken_by_region_name():
    _fresh()
    df = pd.DataFrame(
        {"date": pd.to_datetime(["2024-01-01"] * 3), "region": ["zeta", "alpha", "mid"], "amount": [5.0, 5.0, 9.0]}
    )
    ax = sales_dashboard(df).axes[1]
    assert [t.get_text() for t in ax.get_xticklabels()] == ["mid", "alpha", "zeta"]


# ---- 14-16: order amounts ----


def test_14_five_bins():
    _fresh()
    ax = sales_dashboard(_orders()).axes[2]
    assert len(ax.patches) == 5


def test_15_bar_heights_are_the_histogram_counts():
    _fresh()
    df = _orders()
    ax = sales_dashboard(df).axes[2]
    counts, _ = np.histogram(df["amount"], bins=5)
    assert [p.get_height() for p in ax.patches] == counts.tolist()


def test_16_counts_add_up_to_the_number_of_orders():
    _fresh()
    ax = sales_dashboard(_orders()).axes[2]
    assert sum(p.get_height() for p in ax.patches) == 8
