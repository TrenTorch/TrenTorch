def dispatch(query, routes, fallback):
    q = query.lower()
    for keyword, fn in routes:
        if keyword in q:
            return fn(query)
    return fallback(query)
