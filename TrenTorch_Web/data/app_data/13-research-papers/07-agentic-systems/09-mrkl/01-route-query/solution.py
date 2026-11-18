def route_query(query, experts):
    q = query.lower()
    for keyword, name in experts:
        if keyword in q:
            return name
    return None
