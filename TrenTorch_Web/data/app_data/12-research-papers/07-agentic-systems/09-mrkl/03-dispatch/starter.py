def dispatch(query, routes, fallback):
    """
    query: the user's question
    routes: list of (keyword, function) pairs, checked in order
    fallback: function used when no keyword matches

    Returns:
        The result of the first matching route's function, or of the fallback.
    """
    # TODO: Run the first route whose keyword matches the query, otherwise the fallback (see Theory).
    pass
