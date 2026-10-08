"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/05-paged-attention/01-num-blocks/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vllm-num-blocks")
vllm_num_blocks = _module.vllm_num_blocks


def test_1_exact_fit():
    assert vllm_num_blocks(32, 16) == 2


def test_2_partial_block_is_allocated():
    assert vllm_num_blocks(33, 16) == 3


def test_3_one_token_needs_one_block():
    assert vllm_num_blocks(1, 16) == 1


def test_4_empty_sequence_needs_no_blocks():
    assert vllm_num_blocks(0, 16) == 0


def test_5_returns_an_integer():
    assert isinstance(vllm_num_blocks(5, 2), int)


def test_6_block_size_one_gives_token_count():
    assert vllm_num_blocks(7, 1) == 7

