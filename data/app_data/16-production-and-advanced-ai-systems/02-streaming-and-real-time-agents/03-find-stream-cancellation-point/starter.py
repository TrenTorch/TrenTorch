def find_cancel_point(events: list[tuple[str, str]]) -> int | None:
    """Each event is (event_type, payload), where event_type is one of
    "chunk", "tool_call", "done", or "cancel". Return the index of the
    first "cancel" event, or None if the stream was never cancelled.
    """
    # TODO: implement
    pass
