"""
pytest data/app_data/12-research-papers/07-agentic-systems/07-voyager/01-add-skill/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-voyager-add-skill")
add_skill = _module.add_skill


def test_1_adds_the_skill():
    assert add_skill({}, "mine", "code") == {"mine": "code"}


def test_2_existing_skills_are_kept():
    assert add_skill({"a": "1"}, "b", "2") == {"a": "1", "b": "2"}


def test_3_overwrites_a_skill_with_the_same_name():
    assert add_skill({"a": "old"}, "a", "new") == {"a": "new"}


def test_4_does_not_mutate_the_original_library():
    lib = {"a": "1"}
    add_skill(lib, "b", "2")
    assert lib == {"a": "1"}


def test_5_returns_a_dict():
    assert isinstance(add_skill({}, "x", "y"), dict)


def test_6_empty_name_is_stored_like_any_other():
    assert add_skill({}, "", "c") == {"": "c"}

