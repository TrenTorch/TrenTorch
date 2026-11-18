"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
total_variation = _module.total_variation


def test_1_constant_image_is_zero():
    assert total_variation(np.full((4, 4), 7.0)) == 0.0


def test_2_hand_computed():
    img = np.array([[0.0, 1.0], [3.0, 3.0]])
    # vertical diffs: |3-0|, |3-1| -> mean 2.5 ; horizontal: |1-0|, |3-3| -> mean 0.5
    assert np.isclose(total_variation(img), 0.5 * (2.5 + 0.5))


def test_3_ramp_has_constant_variation():
    img = np.tile(np.arange(5.0), (5, 1))
    assert np.isclose(total_variation(img), 0.5 * (0.0 + 1.0))


def test_4_noise_is_penalized_more_than_a_smooth_image():
    rng = np.random.RandomState(0)
    smooth = np.add.outer(np.arange(8.0), np.arange(8.0)) / 14
    assert total_variation(smooth + rng.rand(8, 8)) > total_variation(smooth)


def test_5_channels_first_images_use_the_last_two_axes():
    img = np.random.RandomState(1).rand(3, 6, 6)
    per_channel = np.mean([total_variation(c) for c in img])
    assert np.isclose(total_variation(img), per_channel)


def test_6_scales_linearly_with_contrast():
    img = np.random.RandomState(2).rand(5, 5)
    assert np.isclose(total_variation(3 * img), 3 * total_variation(img))


def test_7_input_untouched_and_nonnegative():
    img = np.random.RandomState(3).randn(4, 4)
    snap = img.copy()
    assert total_variation(img) >= 0 and np.array_equal(img, snap)
