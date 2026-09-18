"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/04-deduplication/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
jaccard_similarity = _module.jaccard_similarity
deduplicate_documents = _module.deduplicate_documents


def test_identical_token_sets_have_similarity_one():
    assert jaccard_similarity(["a", "b", "c"], ["a", "b", "c"]) == 1.0


def test_disjoint_token_sets_have_similarity_zero():
    assert jaccard_similarity(["a", "b"], ["c", "d"]) == 0.0


def test_partial_overlap_similarity():
    # {a,b,c} vs {b,c,d}: intersection {b,c} (2), union {a,b,c,d} (4) -> 0.5
    assert jaccard_similarity(["a", "b", "c"], ["b", "c", "d"]) == 0.5


def test_similarity_ignores_duplicate_tokens_within_a_document():
    # {a,a,b} has the same SET as {a,b}; repeated tokens don't inflate similarity.
    assert jaccard_similarity(["a", "a", "b"], ["a", "b"]) == 1.0


def test_deduplicate_keeps_all_distinct_documents_below_threshold():
    documents = [["a", "b"], ["c", "d"], ["e", "f"]]
    kept = deduplicate_documents(documents, threshold=0.9)
    assert kept == [0, 1, 2]


def test_deduplicate_removes_exact_duplicates():
    documents = [["a", "b", "c"], ["a", "b", "c"], ["x", "y", "z"]]
    kept = deduplicate_documents(documents, threshold=0.9)
    assert kept == [0, 2]


def test_deduplicate_removes_near_duplicates_above_threshold():
    documents = [["a", "b", "c", "d"], ["a", "b", "c", "e"], ["x", "y", "z", "w"]]
    # similarity(doc0, doc1) = |{a,b,c}| / |{a,b,c,d,e}| = 3/5 = 0.6
    kept = deduplicate_documents(documents, threshold=0.5)
    assert kept == [0, 2]


def test_deduplicate_keeps_near_duplicates_below_threshold():
    documents = [["a", "b", "c", "d"], ["a", "b", "c", "e"]]
    kept = deduplicate_documents(documents, threshold=0.9)  # 0.6 < 0.9, both kept
    assert kept == [0, 1]


def test_deduplicate_compares_against_kept_documents_not_just_the_immediately_previous_one():
    # Directly targets a mutant that only compares each document against
    # the PREVIOUS one, rather than every already-kept document.
    documents = [["a", "b", "c"], ["x", "y", "z"], ["a", "b", "c"]]
    # doc2 duplicates doc0 (kept), even though doc1 (also kept) is different.
    kept = deduplicate_documents(documents, threshold=0.9)
    assert kept == [0, 1]
