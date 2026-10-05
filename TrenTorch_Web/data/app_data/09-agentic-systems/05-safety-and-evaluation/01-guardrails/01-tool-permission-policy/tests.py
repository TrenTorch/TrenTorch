"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
check_permission = _module.check_permission
POLICY = {"allow": ["read:*", "bash:ls*", "bash:git *"], "ask": ["bash:git push*"], "deny": ["bash:rm *", "read:/etc/*"]}


def test_1_allowed_call():
    assert check_permission("read:notes.txt", POLICY) == "allow"


def test_2_deny_beats_allow():
    assert check_permission("read:/etc/passwd", POLICY) == "deny"


def test_3_ask_beats_allow():
    assert check_permission("bash:git push origin main", POLICY) == "ask"
    assert check_permission("bash:git status", POLICY) == "allow"


def test_4_unlisted_calls_default_to_deny():
    assert check_permission("email:send", POLICY) == "deny"


def test_5_wildcards_cross_spaces_and_slashes():
    assert check_permission("bash:rm -rf /tmp/x", POLICY) == "deny"


def test_6_matching_is_case_sensitive():
    assert check_permission("READ:notes.txt", POLICY) == "deny"


def test_7_missing_keys_and_policy_untouched():
    snap = {k: list(v) for k, v in POLICY.items()}
    assert check_permission("anything", {}) == "deny" and check_permission("x", {"allow": ["x"]}) == "allow"
    check_permission("bash:ls", POLICY)
    assert POLICY == snap
