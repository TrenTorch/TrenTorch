"""
pytest data/app_data/03-dl-training/02-layers/04-weight-initialization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/02-layers/{Path(__file__).resolve().parent.name}")
xavier_uniform_bound = _module.xavier_uniform_bound
xavier_normal_std = _module.xavier_normal_std
kaiming_uniform_bound = _module.kaiming_uniform_bound
kaiming_normal_std = _module.kaiming_normal_std


def test_xavier_uniform_bound_matches_hand_computation():
    result = xavier_uniform_bound(fan_in=10, fan_out=5)
    assert np.isclose(result, np.sqrt(6.0 / 15.0))


def test_xavier_normal_std_matches_hand_computation():
    result = xavier_normal_std(fan_in=10, fan_out=5)
    assert np.isclose(result, np.sqrt(2.0 / 15.0))


def test_xavier_is_symmetric_in_fan_in_and_fan_out():
    a = xavier_uniform_bound(fan_in=10, fan_out=20)
    b = xavier_uniform_bound(fan_in=20, fan_out=10)
    assert np.isclose(a, b)


def test_kaiming_uniform_bound_matches_hand_computation_with_default_gain():
    result = kaiming_uniform_bound(fan_in=10)
    expected = np.sqrt(2.0) * np.sqrt(3.0 / 10.0)
    assert np.isclose(result, expected)


def test_kaiming_normal_std_matches_hand_computation_with_default_gain():
    result = kaiming_normal_std(fan_in=10)
    expected = np.sqrt(2.0) / np.sqrt(10.0)
    assert np.isclose(result, expected)


def test_kaiming_respects_a_custom_gain():
    result = kaiming_normal_std(fan_in=4, gain=1.0)
    assert np.isclose(result, 0.5)


def test_kaiming_uniform_bound_squared_matches_three_times_kaiming_normal_variance():
    # Uniform(-a, a) has variance a^2 / 3, so a uniform bound derived from
    # the same target variance as a normal std must satisfy a^2 = 3 * std^2.
    fan_in = 25
    a = kaiming_uniform_bound(fan_in)
    std = kaiming_normal_std(fan_in)
    assert np.isclose(a**2, 3.0 * std**2)


def test_xavier_uniform_bound_squared_matches_three_times_xavier_normal_variance():
    fan_in, fan_out = 10, 20
    a = xavier_uniform_bound(fan_in, fan_out)
    std = xavier_normal_std(fan_in, fan_out)
    assert np.isclose(a**2, 3.0 * std**2)


def test_kaiming_gives_larger_variance_than_xavier_for_the_same_fan_in_used_as_fan_out():
    # Kaiming is designed to compensate for ReLU zeroing out half its
    # input, so it should target strictly more variance than Xavier does
    # for a comparable fan_in/fan_out.
    fan = 16
    xavier_std = xavier_normal_std(fan_in=fan, fan_out=fan)
    kaiming_std = kaiming_normal_std(fan_in=fan)
    assert kaiming_std > xavier_std


def test_all_bounds_are_positive():
    assert xavier_uniform_bound(10, 5) > 0
    assert xavier_normal_std(10, 5) > 0
    assert kaiming_uniform_bound(10) > 0
    assert kaiming_normal_std(10) > 0


def test_kaiming_uniform_bound_uses_gain_not_gain_squared():
    # Directly targets a mutant that squares gain inside the sqrt (a
    # plausible slip when translating gain^2/fan_in into the uniform-bound
    # form), which would change the result's scale entirely for any
    # gain != 1.
    result = kaiming_uniform_bound(fan_in=3, gain=2.0)
    expected = 2.0 * np.sqrt(3.0 / 3.0)  # = 2.0
    assert np.isclose(result, expected)
    wrong_if_squared = (2.0**2) * np.sqrt(3.0 / 3.0)  # = 4.0
    assert not np.isclose(result, wrong_if_squared)
