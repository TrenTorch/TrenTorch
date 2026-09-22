"""
pytest data/app_data/01-classical-ml/05-instance-based-probabilistic/07-amazon-item-to-item-cf/tests.py
"""

import math
import random
import sys
import time
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"99-potd/01-daily/{Path(__file__).resolve().parent.name}"
)
recommend = _module.recommend


def _brute_force(num_users, num_items, purchases, cart, k):
    """Dense and obvious: score every item against every cart item."""
    buyers = {}
    for user, item in purchases:
        buyers.setdefault(item, set()).add(user)
    cart_set = set(cart)
    scored = []
    for j in range(num_items):
        if j in cart_set:
            continue
        total = 0.0
        for c in sorted(cart_set):
            pc, pj = buyers.get(c, set()), buyers.get(j, set())
            if pc and pj:
                total += len(pc & pj) / (math.sqrt(len(pc)) * math.sqrt(len(pj)))
        if total > 0:
            scored.append((j, total))
    scored.sort(key=lambda pair: (-round(pair[1], 9), pair[0]))
    return scored[:k]


def _assert_same(result, expected):
    assert [item for item, _ in result] == [item for item, _ in expected]
    for (_, got), (_, want) in zip(result, expected):
        assert abs(got - want) < 1e-9


EXAMPLE_ONE_EVENTS = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 1), (2, 3), (3, 0), (3, 4)]


def test_example_one_matches_the_specs_worked_derivation():
    result = recommend(4, 5, EXAMPLE_ONE_EVENTS, [0, 1], 2)
    # Item 2 shares a buyer with both cart items. Items 3 and 4 each match one
    # cart item and tie at 1/sqrt(3), so the smaller id (3) wins second place.
    assert [item for item, _ in result] == [2, 3]
    assert abs(result[0][1] - 1.154701) < 1e-6
    assert abs(result[1][1] - 0.577350) < 1e-6


def test_example_two_ties_go_to_the_smaller_item_id():
    events = [(0, 0), (0, 1), (1, 0), (1, 2), (2, 3)]
    result = recommend(3, 4, events, [0], 1)
    assert [item for item, _ in result] == [1]
    assert abs(result[0][1] - 0.707107) < 1e-6


def test_repeated_purchases_by_the_same_user_count_once():
    once = recommend(4, 5, EXAMPLE_ONE_EVENTS, [0, 1], 3)
    noisy = EXAMPLE_ONE_EVENTS + [(0, 0)] * 5 + [(1, 1)] * 4 + [(0, 2)] * 3
    _assert_same(recommend(4, 5, noisy, [0, 1], 3), once)


def test_items_in_the_cart_are_never_recommended():
    # Items 0 and 1 are near-identical, but both are already in the cart.
    events = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 2)]
    result = recommend(3, 3, events, [0, 1], 3)
    assert all(item not in (0, 1) for item, _ in result)
    assert [item for item, _ in result] == [2]


def test_a_cart_that_shares_no_buyers_with_the_catalog_returns_nothing():
    events = [(0, 0), (1, 0), (2, 1), (3, 2)]
    assert recommend(4, 4, events, [3], 5) == []


def test_only_items_with_a_positive_score_are_returned():
    result = recommend(4, 5, EXAMPLE_ONE_EVENTS, [0, 1], 10)
    assert [item for item, _ in result] == [2, 3, 4]


def test_a_cart_item_nobody_bought_is_ignored_without_crashing():
    events = [(0, 0), (1, 0), (1, 1)]
    with_dead_item = recommend(2, 4, events, [0, 3], 3)
    assert [item for item, _ in with_dead_item] == [1]
    assert recommend(2, 4, events, [3], 3) == []


def test_a_cart_item_listed_twice_counts_once():
    once = recommend(4, 5, EXAMPLE_ONE_EVENTS, [0, 1], 3)
    twice = recommend(4, 5, EXAMPLE_ONE_EVENTS, [0, 1, 1, 0], 3)
    _assert_same(twice, once)


def test_many_tied_items_come_back_in_ascending_id_order():
    # Every candidate was bought by exactly one shared user and nobody else.
    events = [(0, 0)] + [(0, j) for j in (7, 3, 9, 5, 1)]
    result = recommend(1, 10, events, [0], 4)
    assert [item for item, _ in result] == [1, 3, 5, 7]


def test_matches_a_brute_force_dense_reference_on_random_inputs():
    rng = random.Random(20260920)
    for _ in range(40):
        users, items = rng.randint(2, 30), rng.randint(2, 25)
        purchases = [(rng.randrange(users), rng.randrange(items)) for _ in range(rng.randint(0, 120))]
        cart = [rng.randrange(items) for _ in range(rng.randint(1, 4))]
        k = rng.randint(1, 8)
        _assert_same(
            recommend(users, items, purchases, cart, k),
            _brute_force(users, items, purchases, cart, k),
        )


def test_an_item_bought_by_almost_everyone_does_not_slow_the_search():
    # The "Harry Potter" case: item 0 is bought by 90% of the users. Comparing
    # every user against every item would be 20_000 x 20_000 operations.
    users = items = 20_000
    purchases = [(u, 0) for u in range(18_000)]
    purchases += [(u, 1 + (u % 200)) for u in range(users)]
    cart = [1]

    start = time.perf_counter()
    result = recommend(users, items, purchases, cart, 5)
    elapsed = time.perf_counter() - start

    assert elapsed < 3.0
    _assert_same(result, _brute_force(users, 300, purchases, cart, 5))
    assert result[0][0] == 0


def test_a_huge_sparse_catalog_never_builds_an_item_by_item_matrix():
    users = items = 100_000
    rng = random.Random(7)
    purchases = [(u, rng.randrange(items)) for u in range(users) for _ in range(2)]
    cart = [purchases[0][1], purchases[1000][1], purchases[50_000][1]]

    tracemalloc.start()
    try:
        result = recommend(users, items, purchases, cart, 5)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    # A 100_000 x 100_000 matrix is 80 GB of float64. The sparse walk needs
    # dictionaries over the ~200_000 events, a small fraction of this budget.
    assert peak < 150 * 1024 * 1024
    scores = [score for _, score in result]
    assert scores == sorted(scores, reverse=True)
    assert all(item not in cart for item, _ in result)
