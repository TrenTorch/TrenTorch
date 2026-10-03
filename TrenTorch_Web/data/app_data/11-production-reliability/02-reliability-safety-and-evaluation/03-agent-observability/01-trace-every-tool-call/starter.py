def build_trace(events: list[tuple[str, str, float]]) -> list[dict]:
    """Each event is (name, kind, duration) where duration is in seconds and
    events run one after another (no overlap). Return a list of dicts, one
    per event, each with keys "name", "kind", "start_offset" (seconds since
    the run began), and "duration", in the given order.
    """
    # TODO: implement
    pass
