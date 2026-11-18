def process_event_queue(events: list[tuple[float, str, str]], handlers: dict[str, str]) -> list[str]:
    """Each event is (timestamp, event_type, payload); events can arrive out
    of order (e.g. from concurrent producers) and must be processed in
    timestamp order, not the order given. `handlers` maps an event_type to a
    format string with a single "{}" placeholder for the payload. For each
    event, in timestamp order, if its event_type has a handler, append
    `handlers[event_type].format(payload)` to the result. Event types with
    no handler are skipped.
    """
    # TODO: implement
    pass
