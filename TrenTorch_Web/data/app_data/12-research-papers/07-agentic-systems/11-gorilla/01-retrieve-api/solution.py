def retrieve_api(query, api_docs):
    q_words = set(query.lower().split())

    def overlap(desc):
        return len(q_words & set(desc.lower().split()))

    best = None
    for name, desc in api_docs.items():
        if best is None or overlap(desc) > overlap(api_docs[best]):
            best = name
    return best
