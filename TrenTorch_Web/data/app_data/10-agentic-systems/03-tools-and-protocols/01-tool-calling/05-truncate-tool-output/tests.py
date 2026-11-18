"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
truncate_to_budget = _module.truncate_to_budget


def test_1_short_text_is_returned_unchanged():
    assert truncate_to_budget("a  b\nc", 5) == "a  b\nc"


def test_2_head_and_tail_hand_computed():
    text = " ".join(str(i) for i in range(1, 11))
    assert truncate_to_budget(text, 4, 0.5) == "1 2 [... 6 tokens omitted ...] 9 10"


def test_3_head_fraction_shifts_the_split():
    text = " ".join(str(i) for i in range(1, 11))
    assert truncate_to_budget(text, 4, 0.75) == "1 2 3 [... 6 tokens omitted ...] 10"


def test_4_zero_tail_edge_case():
    text = " ".join(str(i) for i in range(1, 11))
    assert truncate_to_budget(text, 3, 1.0) == "1 2 3 [... 7 tokens omitted ...]"


def test_5_zero_head_keeps_only_the_tail():
    text = " ".join(str(i) for i in range(1, 11))
    assert truncate_to_budget(text, 3, 0.0) == "[... 7 tokens omitted ...] 8 9 10"


def test_6_exactly_at_budget_is_unchanged():
    assert truncate_to_budget("a b c", 3) == "a b c"


def test_7_output_keeps_exactly_the_budget_of_real_tokens():
    text = " ".join(f"w{i}" for i in range(500))
    out = truncate_to_budget(text, 50, 0.3).split()
    marker_tokens = 5
    assert len(out) == 50 + marker_tokens and out[0] == "w0" and out[-1] == "w499"
