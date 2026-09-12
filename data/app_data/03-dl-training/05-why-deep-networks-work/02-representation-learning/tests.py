"""
pytest data/app_data/03-dl-training/05-why-deep-networks-work/02-representation-learning/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/05-why-deep-networks-work/{Path(__file__).resolve().parent.name}")
lookup_table_size = _module.lookup_table_size
shared_feature_layer_size = _module.shared_feature_layer_size
capacity_ratio = _module.capacity_ratio


def test_lookup_table_size_matches_hand_computation():
    assert lookup_table_size(3) == 8
    assert lookup_table_size(10) == 1024


def test_lookup_table_size_of_zero_features_is_one():
    assert lookup_table_size(0) == 1


def test_shared_feature_layer_size_matches_hand_computation():
    # 4 features, 5 hidden units: 4*5 + 5 = 25
    assert shared_feature_layer_size(4, 5) == 25


def test_shared_feature_layer_size_scales_linearly_with_num_features():
    small = shared_feature_layer_size(10, 8)
    large = shared_feature_layer_size(20, 8)
    # doubling num_features should roughly double the parameter count
    # (ignoring the fixed +num_hidden bias term)
    assert large < 2.5 * small


def test_capacity_ratio_matches_direct_division():
    result = capacity_ratio(5, 4)
    expected = lookup_table_size(5) / shared_feature_layer_size(5, 4)
    assert result == expected


def test_capacity_ratio_grows_much_faster_than_linearly_with_num_features():
    ratio_small = capacity_ratio(10, 16)
    ratio_large = capacity_ratio(20, 16)
    # lookup table size grows exponentially (2^10 -> 2^20, a factor of
    # 1024), while the shared layer only grows linearly, so the ratio
    # should grow by a huge factor, not merely double.
    assert ratio_large > 100 * ratio_small


def test_capacity_ratio_can_be_less_than_one_for_very_few_features():
    # With very few features, the shared layer can actually be LARGER
    # than the lookup table (small num_features, larger num_hidden).
    result = capacity_ratio(2, 50)
    assert result < 1.0


def test_lookup_table_size_uses_two_to_the_power_not_a_linear_count():
    # Directly targets a mutant that computes lookup_table_size as
    # `2 * num_features` (linear) instead of `2 ** num_features`
    # (exponential), which would completely defeat the exponential-growth
    # point this question is built to demonstrate numerically.
    assert lookup_table_size(6) == 64
    assert lookup_table_size(6) != 12
