"""
pytest tests.py
"""

from _load import load_solution

pick_best_past_plan = load_solution(__file__).pick_best_past_plan


def test_1_single_matching_plan():
    past_plans = [("book_flight", "search then confirm", 0.9)]
    assert pick_best_past_plan("book_flight", past_plans) == "search then confirm"


def test_2_picks_highest_success_rate_among_matches():
    past_plans = [
        ("book_flight", "plan A", 0.6),
        ("book_flight", "plan B", 0.9),
        ("book_flight", "plan C", 0.7),
    ]
    assert pick_best_past_plan("book_flight", past_plans) == "plan B"


def test_3_no_match_returns_none():
    past_plans = [("book_hotel", "plan A", 0.9)]
    assert pick_best_past_plan("book_flight", past_plans) is None


def test_4_ignores_plans_for_other_tasks_even_with_higher_rates():
    past_plans = [
        ("book_hotel", "hotel plan", 0.99),
        ("book_flight", "flight plan", 0.5),
    ]
    assert pick_best_past_plan("book_flight", past_plans) == "flight plan"


def test_5_tie_broken_by_first_seen():
    past_plans = [
        ("book_flight", "plan first", 0.8),
        ("book_flight", "plan second", 0.8),
    ]
    assert pick_best_past_plan("book_flight", past_plans) == "plan first"


def test_6_empty_history_returns_none():
    assert pick_best_past_plan("book_flight", []) is None


def test_7_task_name_matching_is_exact_not_substring():
    past_plans = [("book_flight_international", "plan A", 0.9)]
    assert pick_best_past_plan("book_flight", past_plans) is None
