"""
pytest data/app_data/08-systems-performance/01-profiling/02-parameter-counting/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/01-profiling/{Path(__file__).resolve().parent.name}")
count_parameters = _module.count_parameters
count_trainable_parameters = _module.count_trainable_parameters


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_single_array_matches_its_own_size():
    params = [np.zeros((3, 4))]
    assert count_parameters(params) == 12


def test_02_multiple_arrays_sum_together():
    params = [np.zeros((3, 4)), np.zeros(4)]  # a (3,4) weight + (4,) bias
    assert count_parameters(params) == 12 + 4


# --- Shape / general-case coverage -----------------------------------


def test_03_matches_a_real_linear_layers_parameter_count():
    # weight (out_features=4, in_features=10), bias (4,) -- exactly what
    # torch.nn.Linear(10, 4) holds: 10*4 + 4 = 44 parameters.
    weight = np.zeros((4, 10))
    bias = np.zeros(4)
    assert count_parameters([weight, bias]) == 44


def test_04_matches_a_real_conv2d_layers_parameter_count():
    # weight (out_channels=8, in_channels=3, 3, 3), bias (8,) -- exactly
    # what torch.nn.Conv2d(3, 8, kernel_size=3) holds: 3*8*3*3 + 8 = 224.
    weight = np.zeros((8, 3, 3, 3))
    bias = np.zeros(8)
    assert count_parameters([weight, bias]) == 224


# --- Parameter handling -------------------------------------------------


def test_05_trainable_count_excludes_frozen_parameters():
    weight = np.zeros((4, 10))  # 40, trainable
    bias = np.zeros(4)  # 4, frozen
    total = count_parameters([weight, bias])
    trainable = count_trainable_parameters([weight, bias], [True, False])
    assert total == 44
    assert trainable == 40


def test_06_all_frozen_gives_zero_trainable_parameters():
    params = [np.zeros((3, 3)), np.zeros(5)]
    assert count_trainable_parameters(params, [False, False]) == 0


def test_07_all_trainable_matches_total_count():
    params = [np.zeros((3, 3)), np.zeros(5)]
    assert count_trainable_parameters(params, [True, True]) == count_parameters(params)


# --- Edge cases ---------------------------------------------------------


def test_08_empty_parameter_list_gives_zero():
    assert count_parameters([]) == 0
    assert count_trainable_parameters([], []) == 0


def test_09_scalar_shaped_parameter_counts_as_one():
    params = [np.array(5.0)]  # a 0-d array, e.g. a single learned temperature
    assert count_parameters(params) == 1


# --- Array hygiene ------------------------------------------------------


def test_10_does_not_mutate_the_input_arrays():
    weight = np.zeros((3, 4))
    weight_copy = weight.copy()
    count_parameters([weight])
    assert np.array_equal(weight, weight_copy)


# --- Independent correctness oracle -----------------------------------


def test_11_matches_real_pytorch_module_parameter_counts():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   lin = torch.nn.Linear(10, 4)
    #   sum(p.numel() for p in lin.parameters())  # 44
    #   conv = torch.nn.Conv2d(3, 8, kernel_size=3)
    #   sum(p.numel() for p in conv.parameters())  # 224
    #
    # This test needs no torch installed to run.
    linear_params = [np.zeros((4, 10)), np.zeros(4)]
    conv_params = [np.zeros((8, 3, 3, 3)), np.zeros(8)]
    assert count_parameters(linear_params) == 44
    assert count_parameters(conv_params) == 224
