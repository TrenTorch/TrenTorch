"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/06-gpipe/02-micro-batch-size/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gpipe-micro-batch-size")
micro_batch_size = _module.micro_batch_size


def test_1_even_split():
    assert micro_batch_size(32, 4) == 8


def test_2_one_micro_batch_is_the_whole_batch():
    assert micro_batch_size(16, 1) == 16


def test_3_batch_equal_to_micro_gives_one_each():
    assert micro_batch_size(4, 4) == 1


def test_4_uneven_split_rounds_down():
    assert micro_batch_size(10, 3) == 3


def test_5_returns_an_integer():
    assert isinstance(micro_batch_size(8, 2), int)


def test_6_more_micro_batches_means_smaller_ones():
    assert micro_batch_size(64, 8) < micro_batch_size(64, 4)

