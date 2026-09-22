"""pytest data/app_data/16-production-and-advanced-ai-systems/05-synthetic-data-and-self-improvement/02-quality-filter-synthetic-examples/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

filter_quality = load_solution(
    f"16-production-and-advanced-ai-systems/05-synthetic-data-and-self-improvement/{Path(__file__).resolve().parent.name}"
).filter_quality


def test_1_too_short_example_dropped():
    examples = ["ok", "a reasonably long and useful example sentence"]
    assert filter_quality(examples, min_length=10, banned_phrases=[]) == [
        "a reasonably long and useful example sentence"
    ]


def test_2_banned_phrase_dropped():
    examples = ["as an AI language model, I cannot help", "the capital of France is Paris"]
    result = filter_quality(examples, min_length=5, banned_phrases=["as an AI language model"])
    assert result == ["the capital of France is Paris"]


def test_3_banned_phrase_matched_case_insensitively():
    examples = ["AS AN AI LANGUAGE MODEL, sorry"]
    assert filter_quality(examples, min_length=5, banned_phrases=["as an ai language model"]) == []


def test_4_kept_examples_preserve_original_order():
    examples = ["first good example here", "second good example here"]
    assert filter_quality(examples, min_length=5, banned_phrases=["bad phrase"]) == examples


def test_5_empty_examples_returns_empty_list():
    assert filter_quality([], min_length=5, banned_phrases=["x"]) == []
