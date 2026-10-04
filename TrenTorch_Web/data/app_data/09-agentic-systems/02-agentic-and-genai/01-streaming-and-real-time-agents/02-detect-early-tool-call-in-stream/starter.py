def detect_early_tool_call(chunks: list[str], marker: str) -> int | None:
    """Chunks arrive one at a time. As soon as the accumulated text (built up
    from `chunks[0]` through the current chunk) contains `marker` -- the
    signal a tool call is starting -- return the index of the chunk where
    that first became true. If `marker` never appears, return None.
    """
    # TODO: implement
    pass
