"""
pytest data/app_data/12-research-papers/07-agentic-systems/11-gorilla/01-retrieve-api/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gorilla-retrieve-api")
retrieve_api = _module.retrieve_api


def test_1_picks_the_api_with_most_shared_words():
    docs = {"weather": "get the weather forecast", "stocks": "stock prices"}
    assert retrieve_api("what is the weather forecast", docs) == "weather"


def test_2_ties_go_to_the_first_api():
    docs = {"a": "red", "b": "red"}
    assert retrieve_api("red", docs) == "a"


def test_3_matching_is_case_insensitive():
    docs = {"music": "play Song", "news": "headlines"}
    assert retrieve_api("PLAY song now", docs) == "music"


def test_4_single_api_is_returned():
    assert retrieve_api("anything", {"only": "x"}) == "only"


def test_5_empty_docs_return_none():
    assert retrieve_api("q", {}) is None


def test_6_does_not_mutate_docs():
    docs = {"a": "x"}
    retrieve_api("x", docs)
    assert docs == {"a": "x"}

