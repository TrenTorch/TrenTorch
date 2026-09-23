def top_k_hashtags(k: int, captions: list[str]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    first_seen: dict[str, int] = {}
    order = 0

    for caption in captions:
        for token in caption.split():
            if not token.startswith("#"):
                continue
            if token not in counts:
                counts[token] = 0
                first_seen[token] = order
                order += 1
            counts[token] += 1

    ranked = sorted(counts.keys(), key=lambda tag: (-counts[tag], first_seen[tag]))
    return [(tag, counts[tag]) for tag in ranked[:k]]
