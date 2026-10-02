"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
stale_packages = _module.stale_packages


def test_current_lock_has_no_stale_packages():
    assert stale_packages({"numpy": "1.26", "pandas": "2.0"}, {"numpy": "1.26.4", "pandas": "2.2.0"}) == []


def test_missing_package_is_stale():
    assert stale_packages({"numpy": "1.0", "scipy": "1.0"}, {"numpy": "1.2.0"}) == ["scipy"]


def test_locked_below_minimum_is_stale():
    assert stale_packages({"pandas": "2.0"}, {"pandas": "1.5.3"}) == ["pandas"]


def test_numeric_not_string_comparison():
    # "1.10" is newer than "1.9" even though "1.10" < "1.9" as strings.
    assert stale_packages({"pkg": "1.9"}, {"pkg": "1.10"}) == []
    assert stale_packages({"pkg": "1.10"}, {"pkg": "1.9"}) == ["pkg"]


def test_trailing_zeros_do_not_matter():
    assert stale_packages({"pkg": "1.2.0"}, {"pkg": "1.2"}) == []
    assert stale_packages({"pkg": "1.2"}, {"pkg": "1.2.0"}) == []


def test_undeclared_locked_packages_ignored_and_result_sorted():
    declared = {"zeta": "2.0", "alpha": "2.0"}
    locked = {"zeta": "1.0", "alpha": "1.0", "transitive": "9.9"}
    assert stale_packages(declared, locked) == ["alpha", "zeta"]


def test_newer_locked_version_is_not_stale():
    assert stale_packages({"pkg": "1.0"}, {"pkg": "99.0"}) == []
