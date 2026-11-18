"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
lcs_length = _module.lcs_length
trajectory_match = _module.trajectory_match


def test_1_lcs_hand_computed():
    assert lcs_length(list("ABCBDAB"), list("BDCABA")) == 4


def test_2_identical_and_disjoint():
    assert lcs_length(["a", "b"], ["a", "b"]) == 2 and lcs_length(["a"], ["b"]) == 0


def test_3_extra_steps_keep_order_satisfied():
    p, r, ok = trajectory_match(["verify", "noop", "lookup", "refund"], ["verify", "lookup", "refund"])
    assert ok and r == 1.0 and p == 3 / 4


def test_4_wrong_order_fails_in_order_check():
    _, r, ok = trajectory_match(["refund", "lookup", "verify"], ["verify", "lookup", "refund"])
    assert not ok and r == 1 / 3


def test_5_missing_step():
    p, r, ok = trajectory_match(["verify", "refund"], ["verify", "lookup", "refund"])
    assert not ok and p == 1.0 and r == 2 / 3


def test_6_empty_cases():
    assert trajectory_match([], ["a"]) == (0.0, 0.0, False)
    assert trajectory_match(["a"], []) == (0.0, 0.0, True)


def test_7_symmetry_of_lcs_and_inputs_untouched():
    a, b = list("AGGTAB"), list("GXTXAYB")
    sa, sb = list(a), list(b)
    assert lcs_length(a, b) == lcs_length(b, a) == 4 and a == sa and b == sb
