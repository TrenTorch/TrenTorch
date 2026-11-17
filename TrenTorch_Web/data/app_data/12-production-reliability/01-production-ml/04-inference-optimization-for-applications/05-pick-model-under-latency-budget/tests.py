"""pytest tests.py"""

from _load import load_solution

pick_model_under_budget = load_solution(__file__).pick_model_under_budget


MODELS = [
    ("tiny", 0.6, 50.0),
    ("medium", 0.8, 200.0),
    ("large", 0.95, 800.0),
]


def test_1_budget_allows_only_the_cheapest_model():
    assert pick_model_under_budget(MODELS, latency_budget_ms=100.0) == "tiny"


def test_2_budget_allows_the_best_quality_model():
    assert pick_model_under_budget(MODELS, latency_budget_ms=1000.0) == "large"


def test_3_budget_excludes_all_models_returns_none():
    assert pick_model_under_budget(MODELS, latency_budget_ms=10.0) is None


def test_4_budget_exactly_matches_a_models_latency():
    assert pick_model_under_budget(MODELS, latency_budget_ms=200.0) == "medium"


def test_5_tie_in_quality_score_first_one_wins():
    tied = [("a", 0.7, 50.0), ("b", 0.7, 60.0)]
    assert pick_model_under_budget(tied, latency_budget_ms=100.0) == "a"
