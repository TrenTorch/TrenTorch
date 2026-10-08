"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/12-fsdp/03-padded-numel/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-fsdp-padded-numel")
fsdp_padded_numel = _module.fsdp_padded_numel


def test_1_already_divisible_is_unchanged():
    assert fsdp_padded_numel(12, 4) == 12


def test_2_pads_to_next_multiple():
    assert fsdp_padded_numel(10, 4) == 12


def test_3_single_rank_is_unchanged():
    assert fsdp_padded_numel(7, 1) == 7


def test_4_padding_is_less_than_world():
    assert fsdp_padded_numel(10, 4) - 10 < 4


def test_5_returns_an_integer():
    assert isinstance(fsdp_padded_numel(5, 2), int)


def test_6_padded_size_divides_by_world():
    assert fsdp_padded_numel(13, 5) % 5 == 0

