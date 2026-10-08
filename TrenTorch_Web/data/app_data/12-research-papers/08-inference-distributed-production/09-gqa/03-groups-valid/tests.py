"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/09-gqa/03-groups-valid/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gqa-groups-valid")
groups_valid = _module.groups_valid


def test_1_even_split_is_valid():
    assert groups_valid(8, 2) is True


def test_2_uneven_split_is_invalid():
    assert groups_valid(8, 3) is False


def test_3_one_group_is_valid():
    assert groups_valid(8, 1) is True


def test_4_more_groups_than_heads_is_invalid():
    assert groups_valid(4, 8) is False


def test_5_zero_groups_is_invalid():
    assert groups_valid(4, 0) is False


def test_6_returns_a_bool():
    assert isinstance(groups_valid(6, 2), bool)

