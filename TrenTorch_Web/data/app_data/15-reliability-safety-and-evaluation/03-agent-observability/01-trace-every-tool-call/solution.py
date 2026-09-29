def build_trace(events: list[tuple[str, str, float]]) -> list[dict]:
    trace = []
    start_offset = 0.0
    for name, kind, duration in events:
        trace.append({
            "name": name,
            "kind": kind,
            "start_offset": start_offset,
            "duration": duration,
        })
        start_offset += duration
    return trace
