import math
from collections import defaultdict

# Scores within this distance count as tied, so the smaller item id wins.
# Summing floats in a different order can differ in the last bits, and that
# must not decide a tie.
TIE_DECIMALS = 9


def recommend(
    num_users: int,
    num_items: int,
    purchases: list[tuple[int, int]],
    cart: list[int],
    k: int,
) -> list[tuple[int, float]]:
    buyers_of = defaultdict(set)  # item -> P_item, the users who bought it
    items_of = defaultdict(set)  # user -> the items that user bought
    for user, item in purchases:
        buyers_of[item].add(user)
        items_of[user].add(item)

    cart_items = set(cart)
    scores = defaultdict(float)

    for cart_item in cart_items:
        cart_buyers = buyers_of.get(cart_item)
        if not cart_buyers:
            continue

        # |P_cart ∩ P_j| for every candidate j, found by walking only the
        # people who bought the cart item and the items those people bought.
        shared = defaultdict(int)
        for user in cart_buyers:
            for item in items_of[user]:
                if item not in cart_items:
                    shared[item] += 1

        cart_norm = math.sqrt(len(cart_buyers))
        for item, overlap in shared.items():
            scores[item] += overlap / (cart_norm * math.sqrt(len(buyers_of[item])))

    ranked = sorted(scores.items(), key=lambda pair: (-round(pair[1], TIE_DECIMALS), pair[0]))
    return ranked[:k]
