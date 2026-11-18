"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
reciprocal_rank_fusion = _module.reciprocal_rank_fusion


def test_1_single_list_keeps_its_order():
    assert reciprocal_rank_fusion([["a", "b", "c"]]) == ["a", "b", "c"]


def test_2_agreement_beats_a_single_first_place():
    # b is 2nd in both lists; a is 1st in one only
    assert reciprocal_rank_fusion([["a", "b"], ["c", "b"]], k=1) == ["b", "a", "c"]


def test_3_hand_computed_scores_decide_the_order():
    # k=60: a: 1/61 ; b: 1/62 + 1/61 ; c: 1/62
    assert reciprocal_rank_fusion([["a", "b"], ["b", "c"]]) == ["b", "a", "c"]


def test_4_ties_are_broken_by_id():
    assert reciprocal_rank_fusion([["b"], ["a"]]) == ["a", "b"]


def test_5_all_documents_appear_exactly_once():
    out = reciprocal_rank_fusion([["a", "b"], ["c"], ["b", "d", "a"]])
    assert sorted(out) == ["a", "b", "c", "d"]


def test_6_empty_inputs():
    assert reciprocal_rank_fusion([]) == [] and reciprocal_rank_fusion([[], []]) == []


def test_7_larger_k_flattens_rank_differences_and_inputs_untouched():
    lists = [["a", "x"], ["x", "a"], ["a"]]
    snap = [list(l) for l in lists]
    assert reciprocal_rank_fusion(lists, k=60)[0] == "a" and reciprocal_rank_fusion(lists, k=1)[0] == "a"
    assert lists == snap
