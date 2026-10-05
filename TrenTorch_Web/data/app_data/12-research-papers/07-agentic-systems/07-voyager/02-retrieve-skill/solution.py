def retrieve_skill(library, query, score):
    if not library:
        return None
    return max(library, key=lambda name: score(query, name))
