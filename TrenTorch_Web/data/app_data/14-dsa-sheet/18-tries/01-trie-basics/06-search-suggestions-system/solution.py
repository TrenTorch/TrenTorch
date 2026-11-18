from bisect import bisect_left


def suggested_products(products, search_word):
    products = sorted(products)
    out = []
    for i in range(1, len(search_word) + 1):
        prefix = search_word[:i]
        start = bisect_left(products, prefix)
        out.append([p for p in products[start : start + 3] if p.startswith(prefix)])
    return out
