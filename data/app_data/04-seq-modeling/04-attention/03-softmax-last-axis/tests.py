"""
pytest data/app_data/04-seq-modeling/04-attention/03-softmax-last-axis/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/04-attention/{Path(__file__).resolve().parent.name}")
softmax_last_axis = _module.softmax_last_axis


def test_output_shape_matches_input_shape_for_2d():
    Z = np.random.randn(3, 4)
    result = softmax_last_axis(Z)
    assert result.shape == (3, 4)


def test_output_shape_matches_input_shape_for_3d():
    Z = np.random.randn(2, 3, 4)
    result = softmax_last_axis(Z)
    assert result.shape == (2, 3, 4)


def test_output_shape_matches_input_shape_for_4d():
    Z = np.random.randn(2, 3, 5, 6)
    result = softmax_last_axis(Z)
    assert result.shape == (2, 3, 5, 6)


def test_last_axis_sums_to_one_for_every_rank():
    for shape in [(4,), (3, 4), (2, 3, 4), (2, 3, 5, 6)]:
        Z = np.random.randn(*shape)
        result = softmax_last_axis(Z)
        assert np.allclose(result.sum(axis=-1), 1.0)


def test_matches_hand_computation():
    Z = np.array([[[1.0, 2.0, 3.0]]])
    result = softmax_last_axis(Z)
    exp_z = np.exp(Z - np.max(Z))
    expected = exp_z / exp_z.sum()
    assert np.allclose(result, expected)


def test_all_equal_values_give_uniform_distribution():
    Z = np.ones((2, 5))
    result = softmax_last_axis(Z)
    assert np.allclose(result, 0.2)


def test_matches_a_manually_written_last_axis_softmax():
    Z = np.random.randn(3, 4, 5)
    result = softmax_last_axis(Z)
    shift = Z - np.max(Z, axis=-1, keepdims=True)
    expected = np.exp(shift) / np.sum(np.exp(shift), axis=-1, keepdims=True)
    assert np.allclose(result, expected, atol=1e-6)


def test_reshape_round_trip_does_not_scramble_which_values_go_together():
    # Directly targets a mutant that reshapes incorrectly (e.g. using
    # Z.reshape(original_shape[-1], -1), swapping which dimension becomes
    # the "batch" and which becomes the softmax axis): for an array whose
    # last-axis groups are easily distinguishable, this would produce
    # values that sum to 1 along the WRONG axis instead.
    Z = np.array([[10.0, 0.0, 0.0], [0.0, 10.0, 0.0], [0.0, 0.0, 10.0]])
    result = softmax_last_axis(Z)
    # each row's LARGEST value (matching its own row's big entry) should
    # dominate that row specifically
    assert np.argmax(result[0]) == 0
    assert np.argmax(result[1]) == 1
    assert np.argmax(result[2]) == 2
