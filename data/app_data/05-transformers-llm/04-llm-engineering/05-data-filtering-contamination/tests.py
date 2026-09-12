"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/05-data-filtering-contamination/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
get_ngrams = _module.get_ngrams
has_contamination = _module.has_contamination
filter_contaminated_documents = _module.filter_contaminated_documents


def test_get_ngrams_basic():
    result = get_ngrams(["a", "b", "c", "d"], n=2)
    assert result == {("a", "b"), ("b", "c"), ("c", "d")}


def test_get_ngrams_n_equals_length_gives_one_ngram():
    result = get_ngrams(["a", "b", "c"], n=3)
    assert result == {("a", "b", "c")}


def test_get_ngrams_n_greater_than_length_gives_empty_set():
    result = get_ngrams(["a", "b"], n=5)
    assert result == set()


def test_has_contamination_true_on_shared_ngram():
    eval_ngrams = {("the", "quick", "brown")}
    train_doc = ["a", "the", "quick", "brown", "fox"]
    assert has_contamination(train_doc, eval_ngrams, n=3) is True


def test_has_contamination_false_when_no_overlap():
    eval_ngrams = {("the", "quick", "brown")}
    train_doc = ["completely", "different", "words", "here"]
    assert has_contamination(train_doc, eval_ngrams, n=3) is False


def test_filter_keeps_uncontaminated_documents():
    train_documents = [["a", "b", "c", "d"], ["w", "x", "y", "z"]]
    eval_documents = [["p", "q", "r", "s"]]
    kept = filter_contaminated_documents(train_documents, eval_documents, n=2)
    assert kept == [0, 1]


def test_filter_removes_contaminated_documents():
    train_documents = [["the", "cat", "sat", "down"], ["totally", "unrelated", "text", "here"]]
    eval_documents = [["the", "cat", "sat", "quietly"]]
    # "the cat sat" (n=3) appears in both doc0 and the eval set.
    kept = filter_contaminated_documents(train_documents, eval_documents, n=3)
    assert kept == [1]


def test_filter_checks_against_all_eval_documents_not_just_the_first():
    # Directly targets a mutant that only builds n-grams from
    # eval_documents[0], ignoring the rest of the eval set.
    train_documents = [["x", "y", "z", "w"]]
    eval_documents = [["a", "b", "c", "d"], ["x", "y", "z", "extra"]]
    kept = filter_contaminated_documents(train_documents, eval_documents, n=3)
    assert kept == []  # doc0 shares "x y z" with eval_documents[1]


def test_larger_n_is_a_stricter_stronger_signal_fewer_false_positives():
    # A 2-gram match can be coincidental common phrasing; requiring a
    # longer, more specific n-gram match reduces false-positive flags.
    train_documents = [["the", "cat", "sat", "on", "a", "mat"]]
    eval_documents = [["the", "cat", "ran", "far", "away"]]
    kept_n2 = filter_contaminated_documents(train_documents, eval_documents, n=2)  # "the cat" overlaps
    kept_n4 = filter_contaminated_documents(train_documents, eval_documents, n=4)  # no 4-gram overlap
    assert kept_n2 == []
    assert kept_n4 == [0]
