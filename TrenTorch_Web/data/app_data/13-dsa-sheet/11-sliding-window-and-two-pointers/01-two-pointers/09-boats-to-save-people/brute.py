from itertools import permutations


def boats_needed(people, limit):
    best = len(people)
    for order in permutations(people):
        boats = 0
        i = 0
        while i < len(order):
            if i + 1 < len(order) and order[i] + order[i + 1] <= limit:
                i += 2
            else:
                i += 1
            boats += 1
        best = min(best, boats)
    return best
