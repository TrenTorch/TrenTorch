def suggested_products(products: list[str], search_word: str) -> list[list[str]]:
    """After each typed letter, return up to three matching products in dictionary order."""
    # This is correct but too slow: it scans and sorts all the products after every letter.
    out = []
    for i in range(1, len(search_word) + 1):
        prefix = search_word[:i]
        out.append(sorted(p for p in products if p.startswith(prefix))[:3])
    return out
