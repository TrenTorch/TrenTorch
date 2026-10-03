"""
pytest tests.py
"""

import math
from _load import load_solution

_module = load_solution(__file__)
trainable_mask = _module.trainable_mask
count_trainable = _module.count_trainable
fraction_trainable = _module.fraction_trainable
NAMES = ["embed.w", "layers.0.w", "layers.0.b", "layers.1.w", "layers.2.w", "head.w"]
SIZES = [100, 40, 4, 40, 40, 10]


def test_1_hand_computed_mask():
    assert trainable_mask(NAMES, 2) == [False, False, False, False, True, True]


def test_2_zero_frozen_trains_everything():
    assert all(trainable_mask(NAMES, 0))


def test_3_freezing_everything_leaves_only_the_head():
    assert trainable_mask(NAMES, 99) == [False, False, False, False, False, True]


def test_4_unrecognised_names_are_trainable():
    assert trainable_mask(["pooler.w"], 5) == [True]


def test_5_count_hand_computed():
    assert count_trainable(SIZES, trainable_mask(NAMES, 2)) == 40 + 10


def test_6_fraction():
    mask = trainable_mask(NAMES, 2)
    assert math.isclose(fraction_trainable(SIZES, mask), 50 / 234)


def test_7_more_freezing_never_increases_trainable_parameters_and_inputs_untouched():
    names, sizes = list(NAMES), list(SIZES)
    counts = [count_trainable(SIZES, trainable_mask(NAMES, k)) for k in range(5)]
    assert counts == sorted(counts, reverse=True) and names == NAMES and sizes == SIZES
