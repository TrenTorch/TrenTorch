from itertools import permutations


def find_order(num_courses, prerequisites):
    for order in permutations(range(num_courses)):
        position = {c: i for i, c in enumerate(order)}
        if all(position[pre] < position[course] for course, pre in prerequisites):
            return list(order)
    return []
