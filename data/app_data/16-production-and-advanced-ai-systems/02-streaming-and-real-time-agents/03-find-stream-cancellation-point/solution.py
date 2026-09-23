def find_cancel_point(events: list[tuple[str, str]]) -> int | None:
    for i, (event_type, _payload) in enumerate(events):
        if event_type == "cancel":
            return i
    return None
