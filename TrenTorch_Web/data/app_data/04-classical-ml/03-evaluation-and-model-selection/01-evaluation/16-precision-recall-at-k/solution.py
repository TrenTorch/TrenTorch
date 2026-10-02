def _hits(ranked, relevant, k):
    relevant = set(relevant)
    return sum(1 for item in ranked[:k] if item in relevant)


def precision_at_k(ranked: list, relevant, k: int) -> float:
    if k <= 0:
        return 0.0
    return _hits(ranked, relevant, k) / k


def recall_at_k(ranked: list, relevant, k: int) -> float:
    relevant = set(relevant)
    if not relevant or k <= 0:
        return 0.0
    return _hits(ranked, relevant, k) / len(relevant)
