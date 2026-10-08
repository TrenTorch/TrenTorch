"""
pytest data/app_data/12-research-papers/07-agentic-systems/11-gorilla/02-name-match/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gorilla-name-match")
api_name_matches = _module.api_name_matches


def test_1_matching_name_returns_true():
    assert api_name_matches("weather(city='Paris')", "weather") is True


def test_2_different_name_returns_false():
    assert api_name_matches("stocks(x)", "weather") is False


def test_3_call_without_arguments_matches():
    assert api_name_matches("news()", "news") is True


def test_4_surrounding_spaces_are_ignored():
    assert api_name_matches("  news (x)", "news") is True


def test_5_returns_a_bool():
    assert isinstance(api_name_matches("a()", "a"), bool)


def test_6_prefix_of_name_does_not_match():
    assert api_name_matches("weather_api(x)", "weather") is False

