import math
import re
from collections import Counter


def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def rank_tools(query, tools, top_k=3):
    docs = {name: Counter(_tokens(desc)) for name, desc in tools.items()}
    n = len(docs)
    df = Counter(w for c in docs.values() for w in c)

    def idf(w):
        return math.log((n + 1) / (df.get(w, 0) + 1)) + 1

    def vec(counts):
        return {w: c * idf(w) for w, c in counts.items()}

    def cosine(a, b):
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        if na == 0 or nb == 0:
            return 0.0
        return sum(v * b.get(w, 0.0) for w, v in a.items()) / (na * nb)

    qv = vec(Counter(_tokens(query)))
    scored = [(-cosine(qv, vec(c)), name) for name, c in docs.items()]
    scored.sort()
    return [name for _, name in scored[:top_k]]
