def process_event_queue(events: list[tuple[float, str, str]], handlers: dict[str, str]) -> list[str]:
    ordered = sorted(events, key=lambda event: event[0])
    results = []
    for _timestamp, event_type, payload in ordered:
        if event_type in handlers:
            results.append(handlers[event_type].format(payload))
    return results
