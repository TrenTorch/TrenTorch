from collections import deque


def reveal_cards(deck):
    n = len(deck)
    result = [0] * n
    positions = deque(range(n))
    for card in sorted(deck):
        result[positions.popleft()] = card
        if positions:
            positions.append(positions.popleft())
    return result
