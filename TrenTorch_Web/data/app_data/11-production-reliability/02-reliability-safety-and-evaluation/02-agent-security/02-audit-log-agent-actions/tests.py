"""pytest tests.py"""

from _load import load_solution

build_audit_log = load_solution(__file__).build_audit_log


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
