def suggested_products(products, search_word):
    out = []
    for i in range(1, len(search_word) + 1):
        prefix = search_word[:i]
        out.append(sorted(p for p in products if p.startswith(prefix))[:3])
    return out
