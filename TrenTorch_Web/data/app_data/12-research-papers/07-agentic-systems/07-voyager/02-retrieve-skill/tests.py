"""
pytest data/app_data/12-research-papers/07-agentic-systems/07-voyager/02-retrieve-skill/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-voyager-retrieve-skill")
retrieve_skill = _module.retrieve_skill


def test_1_returns_the_highest_scoring_skill():
    lib = {"mine_wood": "...", "craft_table": "..."}
    assert retrieve_skill(lib, "craft", lambda q, n: 1.0 if "craft" in n else 0.0) == "craft_table"


def test_2_empty_library_returns_none():
    assert retrieve_skill({}, "anything", lambda q, n: 0.0) is None


def test_3_single_skill_is_returned():
    assert retrieve_skill({"only": "x"}, "q", lambda q, n: 0.0) == "only"


def test_4_score_function_receives_the_query():
    lib = {"a": "", "b": ""}
    assert retrieve_skill(lib, "b", lambda q, n: 1.0 if n == q else 0.0) == "b"


def test_5_returns_a_name_from_the_library():
    lib = {"x": "1", "y": "2"}
    assert retrieve_skill(lib, "q", lambda q, n: len(n)) in lib


def test_6_does_not_mutate_library():
    lib = {"x": "1"}
    retrieve_skill(lib, "q", lambda q, n: 0.0)
    assert lib == {"x": "1"}

