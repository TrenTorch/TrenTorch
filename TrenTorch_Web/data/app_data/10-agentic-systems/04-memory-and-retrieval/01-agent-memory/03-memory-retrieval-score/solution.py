import math


def _cosine(a, b):
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def memory_scores(memories, query, now, decay, weights):
    wr, wi, ws = weights
    return [
        wr * decay ** (now - m["last_access"]) + wi * m["importance"] / 10 + ws * _cosine(query, m["embedding"])
        for m in memories
    ]


def top_memories(memories, query, now, k, decay, weights):
    scores = memory_scores(memories, query, now, decay, weights)
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
    return order[:k]
