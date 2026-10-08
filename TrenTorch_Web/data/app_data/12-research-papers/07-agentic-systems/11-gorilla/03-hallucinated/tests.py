"""
pytest data/app_data/12-research-papers/07-agentic-systems/11-gorilla/03-hallucinated/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gorilla-hallucinated")
is_hallucinated = _module.is_hallucinated


def test_1_known_api_is_not_hallucinated():
    assert is_hallucinated("weather", ["weather", "news"]) is False


def test_2_unknown_api_is_hallucinated():
    assert is_hallucinated("teleport", ["weather", "news"]) is True


def test_3_empty_api_list_flags_everything():
    assert is_hallucinated("anything", []) is True


def test_4_match_is_exact():
    assert is_hallucinated("Weather", ["weather"]) is True


def test_5_returns_a_bool():
    assert isinstance(is_hallucinated("x", ["x"]), bool)


def test_6_list_is_not_modified():
    apis = ["a"]
    is_hallucinated("b", apis)
    assert apis == ["a"]

