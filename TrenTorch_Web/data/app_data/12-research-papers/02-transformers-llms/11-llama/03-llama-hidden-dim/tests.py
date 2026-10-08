"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/11-llama/03-llama-hidden-dim/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-llama-hidden-dim")
llama_hidden_dim = _module.llama_hidden_dim


def test_1_seven_b_model_width_gives_eleven_thousand_eight():
    assert llama_hidden_dim(4096) == 11008


def test_2_result_is_a_multiple_of_the_rounding_unit():
    assert llama_hidden_dim(4096) % 256 == 0


def test_3_result_is_at_least_eight_thirds_of_the_width():
    assert llama_hidden_dim(4096) >= 8 * 4096 / 3


def test_4_custom_rounding_unit_is_respected():
    assert llama_hidden_dim(1000, multiple_of=64) % 64 == 0


def test_5_larger_width_gives_larger_hidden_size():
    assert llama_hidden_dim(8192) > llama_hidden_dim(4096)


def test_6_matches_a_hand_value_for_width_eight_thousand_one_hundred_ninety_two():
    assert llama_hidden_dim(8192) == 22016

