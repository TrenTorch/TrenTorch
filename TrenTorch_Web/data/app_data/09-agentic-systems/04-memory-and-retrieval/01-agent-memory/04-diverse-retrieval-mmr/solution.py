import math


def _cos(a, b):
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def mmr_select(query, docs, k, lam):
    rel = [_cos(query, d) for d in docs]
    chosen, remaining = [], list(range(len(docs)))
    while remaining and len(chosen) < k:
        def score(i):
            red = max((_cos(docs[i], docs[s]) for s in chosen), default=0.0)
            return lam * rel[i] - (1 - lam) * red
        best = max(remaining, key=lambda i: (score(i), -i))
        chosen.append(best)
        remaining.remove(best)
    return chosen
