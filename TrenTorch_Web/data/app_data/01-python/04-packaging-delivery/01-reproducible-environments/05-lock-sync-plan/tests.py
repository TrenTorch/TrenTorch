"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
sync_plan = _module.sync_plan


def test_already_in_sync():
    env = {"numpy": "1.26.4", "pandas": "2.2.0"}
    assert sync_plan(env, dict(env)) == {"install": [], "remove": []}


def test_missing_packages_are_installed():
    plan = sync_plan({"numpy": "1.26.4", "pandas": "2.2.0"}, {"numpy": "1.26.4"})
    assert plan == {"install": ["pandas"], "remove": []}


def test_wrong_version_is_reinstalled():
    plan = sync_plan({"numpy": "1.26.4"}, {"numpy": "1.24.0"})
    assert plan == {"install": ["numpy"], "remove": []}


def test_exact_removes_extraneous():
    plan = sync_plan({"numpy": "1.26.4"}, {"numpy": "1.26.4", "ipdb": "0.13", "black": "24.1"})
    assert plan == {"install": [], "remove": ["black", "ipdb"]}


def test_inexact_keeps_extraneous():
    plan = sync_plan({"numpy": "1.26.4"}, {"numpy": "1.26.4", "ipdb": "0.13"}, exact=False)
    assert plan == {"install": [], "remove": []}


def test_empty_environment():
    plan = sync_plan({"b": "1", "a": "2"}, {})
    assert plan == {"install": ["a", "b"], "remove": []}
