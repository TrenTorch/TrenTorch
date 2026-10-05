def top_k_memories(memories, k):
    ranked = sorted(memories, key=lambda m: -m[1])
    return [name for name, _ in ranked[:k]]
