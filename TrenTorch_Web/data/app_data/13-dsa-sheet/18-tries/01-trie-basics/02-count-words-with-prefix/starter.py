def count_with_prefix(words: list[str], queries: list[str]) -> list[int]:
    """For each query, return how many words start with it."""
    # This is correct but too slow: it checks every word for every query.
    return [sum(1 for w in words if w.startswith(q)) for q in queries]
