def jaccard_similarity(tokens_a: list[str], tokens_b: list[str]) -> float:
    set_a, set_b = set(tokens_a), set(tokens_b)
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def deduplicate_documents(documents: list[list[str]], threshold: float) -> list[int]:
    kept_indices = []
    for i, doc in enumerate(documents):
        is_duplicate = False
        for kept_i in kept_indices:
            if jaccard_similarity(doc, documents[kept_i]) >= threshold:
                is_duplicate = True
                break
        if not is_duplicate:
            kept_indices.append(i)
    return kept_indices
