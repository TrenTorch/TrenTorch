import random


def k_closest(points, k):
    if k <= 0:
        return []
    pool = [((p[0] * p[0] + p[1] * p[1], p[0], p[1]), p) for p in points]
    if k < len(pool):
        chosen = []
        need = k
        while need > 0:
            pivot = random.choice(pool)[0]
            less = [item for item in pool if item[0] < pivot]
            equal = [item for item in pool if item[0] == pivot]
            if need <= len(less):
                pool = less
            elif need <= len(less) + len(equal):
                chosen += less
                chosen += equal[: need - len(less)]
                need = 0
            else:
                chosen += less
                chosen += equal
                need -= len(less) + len(equal)
                pool = [item for item in pool if item[0] > pivot]
        pool = chosen
    pool.sort(key=lambda item: item[0])
    return [p for _, p in pool]
