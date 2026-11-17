from collections import deque
from itertools import permutations


def reveal_cards(deck):
    target = sorted(deck)
    for order in permutations(deck):
        cards = deque(order)
        revealed = []
        while cards:
            revealed.append(cards.popleft())
            if cards:
                cards.append(cards.popleft())
        if revealed == target:
            return list(order)
