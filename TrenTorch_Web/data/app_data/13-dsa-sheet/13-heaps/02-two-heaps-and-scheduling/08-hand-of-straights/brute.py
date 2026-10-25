def is_n_straight_hand(hand, group_size):
    if len(hand) % group_size:
        return False
    cards = sorted(hand)
    while cards:
        start = cards[0]
        for x in range(start, start + group_size):
            if x not in cards:
                return False
            cards.remove(x)
    return True
