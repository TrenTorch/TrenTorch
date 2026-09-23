"""pytest data/app_data/15-reliability-safety-and-evaluation/02-agent-security/05-audit-log-agent-actions/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

build_audit_log = load_solution(
    f"15-reliability-safety-and-evaluation/02-agent-security/{Path(__file__).resolve().parent.name}"
).build_audit_log


def test_1_single_action():
    assert build_audit_log([("10:00:00", "agent-1", "read file report.csv")]) == [
        "[10:00:00] agent-1: read file report.csv"
    ]


def test_2_multiple_actions_preserve_order():
    actions = [
        ("10:00:00", "agent-1", "read file report.csv"),
        ("10:00:02", "agent-1", "call tool send_email"),
        ("10:00:05", "agent-2", "delete record 42"),
    ]
    assert build_audit_log(actions) == [
        "[10:00:00] agent-1: read file report.csv",
        "[10:00:02] agent-1: call tool send_email",
        "[10:00:05] agent-2: delete record 42",
    ]


def test_3_empty_actions_returns_empty_list():
    assert build_audit_log([]) == []


def test_4_different_actors_formatted_independently():
    actions = [("2026-01-01T00:00:00Z", "supervisor", "delegate task"), ("2026-01-01T00:00:01Z", "worker", "execute task")]
    assert build_audit_log(actions) == [
        "[2026-01-01T00:00:00Z] supervisor: delegate task",
        "[2026-01-01T00:00:01Z] worker: execute task",
    ]


def test_5_description_with_colon_preserved():
    assert build_audit_log([("10:00:00", "agent-1", "note: partial failure")]) == [
        "[10:00:00] agent-1: note: partial failure"
    ]
