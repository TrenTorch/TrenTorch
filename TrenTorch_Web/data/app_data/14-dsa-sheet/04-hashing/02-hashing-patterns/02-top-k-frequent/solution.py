import random
from collections import Counter


def top_k_frequent(nums, k):
    pairs = [(-count, value) for value, count in Counter(nums).items()]
    if k <= 0:
        return []
    if k < len(pairs):
        chosen = []
        pool = pairs
        need = k
        while need > 0:
            pivot = random.choice(pool)
            less = [p for p in pool if p < pivot]
            if need <= len(less):
                pool = less
            elif need == len(less) + 1:
                chosen += less
                chosen.append(pivot)
                need = 0
            else:
                chosen += less
                chosen.append(pivot)
                need -= len(less) + 1
                pool = [p for p in pool if p > pivot]
        pairs = chosen
    return [value for _, value in sorted(pairs)]
