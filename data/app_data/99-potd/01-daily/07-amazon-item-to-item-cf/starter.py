import math
from collections import defaultdict


def recommend(
    num_users: int,
    num_items: int,
    purchases: list[tuple[int, int]],
    cart: list[int],
    k: int,
) -> list[tuple[int, float]]:
    """
    "Customers who bought this also bought...": the top k items to recommend
    for a shopping cart, by item-to-item collaborative filtering.

    num_users, num_items: users and items are numbered 0..num_users-1 and
        0..num_items-1.
    purchases: (user, item) purchase events. The same pair can appear more
        than once; a user counts once per item.
    cart: the item ids in the target customer's cart. It is a set: an id
        listed twice counts once.
    k: how many recommendations to return.

    For an item x, P_x is the set of users who bought it, and

        sim(x, y)  = |P_x & P_y| / (sqrt(|P_x|) * sqrt(|P_y|))
        score(j)   = sum of sim(c, j) over every item c in the cart

    with sim = 0 whenever P_x or P_y is empty. Score every item j that is NOT
    in the cart, and return the best k as (item_id, score) pairs, highest
    score first. Scores that agree to 9 decimal places are tied, and a tie
    goes to the smaller item id. Items with a score of 0 are never returned,
    so the list can be shorter than k, or empty.

    The catalog can have 100,000 items: never build an item-by-item matrix.
    """
    # TODO: see Theory for how to avoid the item-by-item matrix.
    pass
