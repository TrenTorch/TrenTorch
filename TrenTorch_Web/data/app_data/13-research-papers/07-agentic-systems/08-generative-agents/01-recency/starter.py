def recency_score(hours, decay=0.995):
    """
    hours: time since the memory was last accessed
    decay: exponential decay factor per hour, in (0, 1]

    Returns:
        The recency score decay ** hours.
    """
    # TODO: Raise the decay factor to the number of hours (see Theory).
    pass
