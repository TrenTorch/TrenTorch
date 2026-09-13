"""
pytest data/app_data/08-systems-performance/05-acceleration/01-vectorize-naive-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/05-acceleration/{Path(__file__).resolve().parent.name}")
naive_dot_product = _module.naive_dot_product
vectorized_dot_product = _module.vectorized_dot_product
compare_speed = _module.compare_speed


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_naive_dot_product_matches_hand_computation():
    assert naive_dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]) == 32.0


def test_02_vectorized_dot_product_matches_hand_computation():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    assert np.isclose(vectorized_dot_product(a, b), 32.0)


# --- Shape / general-case coverage -----------------------------------


def test_03_both_implementations_agree_on_random_data():
    rng = np.random.default_rng(0)
    a = rng.normal(size=50)
    b = rng.normal(size=50)
    naive = naive_dot_product(a.tolist(), b.tolist())
    vectorized = vectorized_dot_product(a, b)
    assert np.isclose(naive, vectorized)


def test_04_compare_speed_reports_matching_results():
    rng = np.random.default_rng(1)
    a = rng.normal(size=1000)
    b = rng.normal(size=1000)
    result = compare_speed(a, b)
    assert np.isclose(result["naive_result"], result["vectorized_result"])


# --- Parameter handling -------------------------------------------------


def test_05_compare_speed_returns_all_expected_keys():
    a = np.array([1.0, 2.0])
    b = np.array([3.0, 4.0])
    result = compare_speed(a, b)
    for key in ["naive_result", "vectorized_result", "naive_time", "vectorized_time", "speedup"]:
        assert key in result


def test_06_vectorized_is_measurably_faster_on_a_large_array():
    # The actual point of the exercise: on a large enough array, the
    # vectorized version genuinely outperforms the naive Python loop by
    # a wide, unambiguous margin -- not a coin-flip on timing noise.
    rng = np.random.default_rng(2)
    n = 200_000
    a = rng.normal(size=n)
    b = rng.normal(size=n)
    result = compare_speed(a, b)
    assert result["speedup"] > 2.0


# --- Edge cases ---------------------------------------------------------


def test_07_single_element_arrays_work():
    assert naive_dot_product([5.0], [3.0]) == 15.0
    assert np.isclose(vectorized_dot_product(np.array([5.0]), np.array([3.0])), 15.0)


def test_08_all_zero_vectors_give_zero():
    a = np.zeros(10)
    b = np.zeros(10)
    result = compare_speed(a, b)
    assert result["naive_result"] == 0.0
    assert result["vectorized_result"] == 0.0


# --- Array hygiene ------------------------------------------------------


def test_09_does_not_mutate_its_inputs():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    a_copy, b_copy = a.copy(), b.copy()
    compare_speed(a, b)
    assert np.array_equal(a, a_copy)
    assert np.array_equal(b, b_copy)


# --- Independent correctness oracle -----------------------------------


def test_10_vectorized_result_matches_numpys_own_dot_directly():
    # Sanity-checks that vectorized_dot_product is a genuine pass-through
    # to NumPy's own (BLAS-backed) dot product, not a hand-rolled
    # reimplementation that happens to agree on small examples.
    rng = np.random.default_rng(3)
    a = rng.normal(size=500)
    b = rng.normal(size=500)
    assert vectorized_dot_product(a, b) == float(np.dot(a, b))
