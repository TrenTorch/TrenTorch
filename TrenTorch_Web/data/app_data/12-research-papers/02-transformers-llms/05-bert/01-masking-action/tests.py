"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/05-bert/01-masking-action/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-bert-masking-action")
masking_action = _module.masking_action


def test_1_small_draws_replace_with_mask():
    assert masking_action(0.0) == "mask"


def test_2_middle_draws_replace_with_random_token():
    assert masking_action(0.85) == "random"


def test_3_large_draws_keep_the_original_token():
    assert masking_action(0.95) == "keep"


def test_4_boundary_at_point_eight_is_random():
    assert masking_action(0.8) == "random"


def test_5_boundary_at_point_nine_is_keep():
    assert masking_action(0.9) == "keep"


def test_6_is_deterministic():
    assert masking_action(0.42) == masking_action(0.42) == "mask"

