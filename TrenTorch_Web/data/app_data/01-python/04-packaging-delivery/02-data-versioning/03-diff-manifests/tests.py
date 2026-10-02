"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
diff_manifests = _module.diff_manifests


def test_identical_versions_have_no_diff():
    version = {"a.csv": "h1", "b.csv": "h2"}
    assert diff_manifests(version, dict(version)) == {"added": [], "removed": [], "modified": []}


def test_added_file():
    assert diff_manifests({"a": "1"}, {"a": "1", "b": "2"}) == {"added": ["b"], "removed": [], "modified": []}


def test_removed_file():
    assert diff_manifests({"a": "1", "b": "2"}, {"a": "1"}) == {"added": [], "removed": ["b"], "modified": []}


def test_modified_file():
    assert diff_manifests({"a": "1"}, {"a": "9"}) == {"added": [], "removed": [], "modified": ["a"]}


def test_mixed_changes_are_sorted():
    old = {"keep": "k", "gone2": "x", "gone1": "y", "edit": "e1"}
    new = {"keep": "k", "edit": "e2", "new2": "n", "new1": "m"}
    assert diff_manifests(old, new) == {
        "added": ["new1", "new2"],
        "removed": ["gone1", "gone2"],
        "modified": ["edit"],
    }


def test_rename_shows_as_remove_plus_add():
    assert diff_manifests({"old.csv": "h"}, {"new.csv": "h"}) == {
        "added": ["new.csv"],
        "removed": ["old.csv"],
        "modified": [],
    }
