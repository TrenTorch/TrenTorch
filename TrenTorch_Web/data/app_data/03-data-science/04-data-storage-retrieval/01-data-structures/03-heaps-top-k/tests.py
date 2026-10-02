"""
pytest tests.py
"""

import random

from _load import load_solution

_module = load_solution(__file__)
MinHeap = _module.MinHeap
heapify = _module.heapify
top_k = _module.top_k
merge_sorted = _module.merge_sorted


def _is_heap(items):
    return all(items[(i - 1) // 2] <= items[i] for i in range(1, len(items)))


# ---- 1-9: the heap ----


def test_1_pop_returns_items_in_ascending_order():
    heap = MinHeap()
    for v in [5, 3, 8, 1, 9, 2]:
        heap.push(v)
    assert [heap.pop() for _ in range(6)] == [1, 2, 3, 5, 8, 9]


def test_2_peek_returns_the_minimum_without_removing_it():
    heap = MinHeap()
    for v in [4, 2, 7]:
        heap.push(v)
    assert heap.peek() == 2 and len(heap) == 3


def test_3_heap_property_holds_after_every_push():
    heap = MinHeap()
    rng = random.Random(0)
    for _ in range(200):
        heap.push(rng.randint(0, 100))
        assert _is_heap(heap.items)


def test_4_heap_property_holds_after_every_pop():
    heap = MinHeap()
    rng = random.Random(1)
    for _ in range(100):
        heap.push(rng.randint(0, 50))
    while len(heap):
        heap.pop()
        assert _is_heap(heap.items)


def test_5_layout_is_the_array_form_of_a_binary_tree():
    heap = MinHeap()
    for v in [3, 1, 2]:
        heap.push(v)
    assert heap.items[0] == 1 and sorted(heap.items) == [1, 2, 3]


def test_6_duplicates_are_kept():
    heap = MinHeap()
    for v in [2, 2, 1, 1]:
        heap.push(v)
    assert [heap.pop() for _ in range(4)] == [1, 1, 2, 2]


def test_7_empty_heap_raises_index_error():
    heap = MinHeap()
    for call in (heap.pop, heap.peek):
        try:
            call()
        except IndexError:
            continue
        raise AssertionError("expected IndexError")


def test_8_works_with_tuples_as_priorities():
    heap = MinHeap()
    heap.push((2, "b"))
    heap.push((1, "z"))
    heap.push((1, "a"))
    assert heap.pop() == (1, "a") and heap.pop() == (1, "z")


def test_9_len_tracks_pushes_and_pops():
    heap = MinHeap()
    assert len(heap) == 0
    heap.push(1)
    heap.push(2)
    heap.pop()
    assert len(heap) == 1


# ---- 10-13: heapify ----


def test_10_heapify_builds_a_valid_heap():
    rng = random.Random(2)
    values = [rng.randint(0, 1000) for _ in range(300)]
    heap = heapify(values)
    assert _is_heap(heap.items) and sorted(heap.items) == sorted(values)


def test_11_heapify_does_not_modify_the_input():
    values = [5, 4, 3, 2, 1]
    heapify(values)
    assert values == [5, 4, 3, 2, 1]


def test_12_popping_a_heapified_list_sorts_it():
    values = [9, 4, 7, 1, 8, 3]
    heap = heapify(values)
    assert [heap.pop() for _ in range(len(values))] == sorted(values)


def test_13_heapify_of_empty_and_single_lists():
    assert len(heapify([])) == 0
    assert heapify([7]).peek() == 7


# ---- 14-18: top k ----


def test_14_top_k_in_descending_order():
    assert top_k([5, 1, 9, 3, 7, 8], 3) == [9, 8, 7]


def test_15_stream_shorter_than_k_returns_everything():
    assert top_k([2, 1], 5) == [2, 1]


def test_16_non_positive_k_returns_an_empty_list():
    assert top_k([1, 2, 3], 0) == [] and top_k([1, 2, 3], -2) == []


def test_17_works_on_a_one_pass_iterator_and_keeps_duplicates():
    assert top_k(iter([4, 4, 4, 1]), 2) == [4, 4]


def test_18_matches_sorting_on_random_data():
    rng = random.Random(3)
    values = [rng.randint(0, 10_000) for _ in range(2000)]
    assert top_k(values, 25) == sorted(values, reverse=True)[:25]


# ---- 19-22: merging ----


def test_19_merges_sorted_lists():
    assert merge_sorted([[1, 4, 7], [2, 5], [3, 6, 9]]) == [1, 2, 3, 4, 5, 6, 7, 9]


def test_20_handles_empty_lists_and_no_lists():
    assert merge_sorted([[], [1, 2], []]) == [1, 2]
    assert merge_sorted([]) == []


def test_21_ties_follow_the_list_order():
    a = [(1, "a"), (2, "a")]
    b = [(1, "b"), (2, "b")]
    merged = merge_sorted([a, b])
    assert [name for _, name in merged] == ["a", "b", "a", "b"]


def test_22_matches_sorted_concatenation_on_random_lists():
    rng = random.Random(4)
    lists = [sorted(rng.randint(0, 100) for _ in range(rng.randint(0, 30))) for _ in range(8)]
    assert merge_sorted(lists) == sorted(v for l in lists for v in l)
