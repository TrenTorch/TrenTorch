"""
Singular/plural agreement helper used by counted CLI output.

The call sites (`tren module status`, `tren module start`, `tren dev
preflight`) are covered where they already have tests, for example
test_start_module_milestone_countdown.py.
"""

import pytest

from platforms.cli.core.text import pluralize


@pytest.mark.parametrize(
    ("word", "count", "expected"),
    [
        ("day", 1, "day"),
        ("day", 0, "days"),
        ("day", 2, "days"),
        ("minute", 1, "minute"),
        ("hour", 1, "hour"),
        ("module", 1, "module"),
        ("change", 1, "change"),
        ("change", 7, "changes"),
    ],
)
def test_pluralize_agrees_with_count(word, count, expected):
    assert pluralize(word, count) == expected
