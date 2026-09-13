"""
pytest data/app_data/11-production-ml/01-experiment-tracking-and-versioning/02-dataset-versioning-hashing/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/01-experiment-tracking-and-versioning/{Path(__file__).resolve().parent.name}")
compute_content_hash = _module.compute_content_hash
hash_rows_naive = _module.hash_rows_naive
hash_rows_canonical = _module.hash_rows_canonical
datasets_are_identical = _module.datasets_are_identical


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_same_bytes_give_the_same_hash_every_time():
    data = b"col_a,col_b\n1,2\n3,4\n"
    assert compute_content_hash(data) == compute_content_hash(data)


def test_02_naive_hash_differs_when_row_order_differs():
    rows_a = [("alice", 1), ("bob", 2)]
    rows_b = [("bob", 2), ("alice", 1)]  # same data, reordered
    assert not datasets_are_identical(hash_rows_naive(rows_a), hash_rows_naive(rows_b))


# --- General-case coverage --------------------------------------------


def test_03_canonical_hash_matches_regardless_of_row_order():
    rows_a = [("alice", 1), ("bob", 2), ("carol", 3)]
    rows_b = [("carol", 3), ("alice", 1), ("bob", 2)]
    assert datasets_are_identical(hash_rows_canonical(rows_a), hash_rows_canonical(rows_b))


def test_04_different_content_always_produces_different_hashes():
    data_a = b"row1,row2"
    data_b = b"row1,row3"
    assert compute_content_hash(data_a) != compute_content_hash(data_b)


def test_05_hash_output_is_a_hex_string_of_the_right_length():
    h = compute_content_hash(b"anything")
    assert isinstance(h, str)
    assert len(h) == 64  # SHA-256 hex digest length
    assert all(c in "0123456789abcdef" for c in h)


# --- Parameter handling -------------------------------------------------


def test_06_canonical_hash_still_detects_genuinely_different_data():
    rows_a = [("alice", 1), ("bob", 2)]
    rows_b = [("alice", 1), ("bob", 999)]  # genuinely different value
    assert not datasets_are_identical(hash_rows_canonical(rows_a), hash_rows_canonical(rows_b))


def test_07_empty_dataset_hashes_consistently():
    assert hash_rows_canonical([]) == hash_rows_canonical([])
    assert hash_rows_naive([]) == hash_rows_naive([])


# --- Edge cases ---------------------------------------------------------


def test_08_single_row_dataset():
    rows = [("only_row", 1)]
    assert datasets_are_identical(hash_rows_canonical(rows), hash_rows_canonical(list(rows)))


def test_09_empty_bytes_still_produce_a_valid_hash():
    h = compute_content_hash(b"")
    assert len(h) == 64


# --- Independent correctness oracle -----------------------------------


def test_10_canonicalization_genuinely_sorts_rather_than_being_a_no_op():
    # Directly targets a mutant that forgets to actually sort (e.g.
    # hash_rows_canonical just calls hash_rows_naive under the hood):
    # a reordered dataset must produce the SAME canonical hash while
    # still producing a DIFFERENT naive hash, proving canonicalization
    # is doing real, order-independent work.
    rows_a = [(3, "c"), (1, "a"), (2, "b")]
    rows_b = [(1, "a"), (2, "b"), (3, "c")]
    assert hash_rows_naive(rows_a) != hash_rows_naive(rows_b)
    assert hash_rows_canonical(rows_a) == hash_rows_canonical(rows_b)
