"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/03-luong-attention/03-local-window/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-luong-local-window")
local_window = _module.local_window


def test_1_window_around_the_center():
    assert local_window(5, 2, 20) == (3, 8)


def test_2_window_is_clipped_at_the_start():
    assert local_window(1, 3, 10) == (0, 5)


def test_3_window_is_clipped_at_the_end():
    assert local_window(9, 3, 10) == (6, 10)


def test_4_window_has_width_at_most_2d_plus_1():
    s, e = local_window(4, 2, 100)
    assert e - s <= 5


def test_5_returns_a_tuple_of_ints():
    s, e = local_window(3, 1, 10)
    assert isinstance(s, int) and isinstance(e, int)


def test_6_very_wide_window_covers_the_sentence():
    assert local_window(2, 50, 6) == (0, 6)

