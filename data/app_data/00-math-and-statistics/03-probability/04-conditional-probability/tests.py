"""
pytest data/app_data/00-math-and-statistics/03-probability/04-conditional-probability/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/03-probability/{Path(__file__).resolve().parent.name}")
marginal_x = _module.marginal_x
marginal_y = _module.marginal_y
conditional_x_given_y = _module.conditional_x_given_y

# A small joint distribution: rows are X in {0, 1}, columns are Y in {0, 1, 2}.
_JOINT = np.array(
    [
        [0.10, 0.20, 0.05],
        [0.15, 0.25, 0.25],
    ]
)


def test_marginal_x_sums_to_one():
    assert np.isclose(marginal_x(_JOINT).sum(), 1.0)


def test_marginal_y_sums_to_one():
    assert np.isclose(marginal_y(_JOINT).sum(), 1.0)


def test_marginal_x_matches_hand_computation():
    # row 0 sum: 0.10+0.20+0.05 = 0.35, row 1: 0.15+0.25+0.25 = 0.65
    result = marginal_x(_JOINT)
    assert np.allclose(result, [0.35, 0.65])


def test_marginal_y_matches_hand_computation():
    # col 0: 0.25, col 1: 0.45, col 2: 0.30
    result = marginal_y(_JOINT)
    assert np.allclose(result, [0.25, 0.45, 0.30])


def test_conditional_x_given_y_sums_to_one():
    result = conditional_x_given_y(_JOINT, y_index=1)
    assert np.isclose(result.sum(), 1.0)


def test_conditional_x_given_y_matches_hand_computation():
    # column 1: [0.20, 0.25], sum=0.45 -> normalized: [0.4444, 0.5556]
    result = conditional_x_given_y(_JOINT, y_index=1)
    assert np.allclose(result, [0.20 / 0.45, 0.25 / 0.45])


def test_conditional_x_given_y_for_each_y_value_all_sum_to_one():
    for y_index in range(_JOINT.shape[1]):
        result = conditional_x_given_y(_JOINT, y_index)
        assert np.isclose(result.sum(), 1.0)


def test_conditional_x_given_y_is_not_just_the_raw_unnormalized_column():
    # Directly targets a mutant that returns joint[:, y_index] directly
    # without dividing by its sum: the raw column here sums to 0.45, not 1.
    result = conditional_x_given_y(_JOINT, y_index=0)
    raw_column = _JOINT[:, 0]
    assert not np.isclose(result.sum(), raw_column.sum())
    assert np.isclose(result.sum(), 1.0)


def test_marginal_x_does_not_confuse_axis_with_marginal_y():
    # Directly targets a mutant that swaps axis=0 and axis=1 between the
    # two marginal functions: on a non-square joint table, this produces
    # a shape mismatch or a clearly wrong set of numbers.
    assert marginal_x(_JOINT).shape == (2,)
    assert marginal_y(_JOINT).shape == (3,)
