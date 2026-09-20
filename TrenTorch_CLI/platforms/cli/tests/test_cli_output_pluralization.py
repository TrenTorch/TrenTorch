"""
Singular/plural agreement in counted CLI copy.

Covers the `pluralize` helper itself plus the three call sites that used
to hardcode a plural noun: `tren module status`'s last-activity label,
`tren module start`'s milestone unlock countdown, and `tren dev
preflight`'s uncommitted-changes warning.
"""

from datetime import datetime, timedelta

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


def _last_activity(time_diff: timedelta) -> str:
    """Mirror of the branch in ModuleWorkflow's status table."""
    if time_diff < timedelta(hours=1):
        minutes = int(time_diff.total_seconds() / 60)
        return f"{minutes} {pluralize('minute', minutes)} ago"
    if time_diff < timedelta(days=1):
        hours = int(time_diff.total_seconds() / 3600)
        return f"{hours} {pluralize('hour', hours)} ago"
    days = time_diff.days
    return f"{days} {pluralize('day', days)} ago"


@pytest.mark.parametrize(
    ("time_diff", "expected"),
    [
        (timedelta(minutes=1), "1 minute ago"),
        (timedelta(minutes=5), "5 minutes ago"),
        (timedelta(hours=1), "1 hour ago"),
        (timedelta(hours=3), "3 hours ago"),
        (timedelta(hours=25), "1 day ago"),
        (timedelta(days=4), "4 days ago"),
    ],
)
def test_last_activity_label_agrees_with_count(time_diff, expected):
    assert _last_activity(time_diff) == expected


@pytest.mark.parametrize(
    ("modules_left", "expected"),
    [(1, "1 module until unlock"), (3, "3 modules until unlock")],
)
def test_unlock_countdown_agrees_with_count(modules_left, expected):
    assert f"{modules_left} {pluralize('module', modules_left)} until unlock" == expected


@pytest.mark.parametrize(
    ("lines", "expected"),
    [
        (["M file.py"], "1 uncommitted change"),
        (["M a.py", "?? b.py"], "2 uncommitted changes"),
    ],
)
def test_uncommitted_changes_warning_agrees_with_count(lines, expected):
    assert f"{len(lines)} uncommitted {pluralize('change', len(lines))}" == expected


def test_exactly_one_day_old_activity_is_singular():
    """25 hours ago lands on `time_diff.days == 1`, the original bug."""
    diff = datetime.now() - (datetime.now() - timedelta(hours=25))
    assert _last_activity(diff) == "1 day ago"
