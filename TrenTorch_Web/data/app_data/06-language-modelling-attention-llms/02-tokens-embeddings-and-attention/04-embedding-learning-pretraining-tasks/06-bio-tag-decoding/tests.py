"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
decode_bio = _module.decode_bio


def test_1_hand_computed():
    tags = ["B-PER", "I-PER", "O", "B-LOC", "O"]
    assert decode_bio(tags) == [("PER", 0, 2), ("LOC", 3, 4)]


def test_2_adjacent_entities_of_the_same_type_are_split_by_b():
    assert decode_bio(["B-PER", "B-PER", "I-PER"]) == [("PER", 0, 1), ("PER", 1, 3)]


def test_3_stray_i_tag_starts_a_span():
    assert decode_bio(["O", "I-ORG", "I-ORG"]) == [("ORG", 1, 3)]


def test_4_type_change_inside_a_run_starts_a_new_span():
    assert decode_bio(["B-PER", "I-LOC"]) == [("PER", 0, 1), ("LOC", 1, 2)]


def test_5_open_span_at_the_end_is_closed():
    assert decode_bio(["O", "B-LOC", "I-LOC"]) == [("LOC", 1, 3)]


def test_6_no_entities_and_empty_input():
    assert decode_bio(["O", "O"]) == [] and decode_bio([]) == []


def test_7_input_untouched_and_spans_do_not_overlap():
    tags = ["B-A", "I-A", "B-B", "O", "I-B", "I-B", "B-A"]
    snap = list(tags)
    spans = decode_bio(tags)
    assert tags == snap and all(a[2] <= b[1] for a, b in zip(spans, spans[1:]))
