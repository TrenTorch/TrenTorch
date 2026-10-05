import math


def memory_scores(memories: list[dict], query: list[float], now: float, decay: float, weights: tuple[float, float, float]) -> list[float]:
    """Weighted sum of recency, importance and relevance for each memory."""
    # TODO
    pass


def top_memories(memories: list[dict], query: list[float], now: float, k: int, decay: float, weights: tuple[float, float, float]) -> list[int]:
    """Indices of the k best memories, best first (ties: lower index)."""
    # TODO
    pass
