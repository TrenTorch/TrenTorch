def truncate_at_stop(text, stops):
    hits = [text.find(s) for s in stops if s]
    hits = [h for h in hits if h != -1]
    if not hits:
        return text, False
    return text[:min(hits)], True


def safe_emit_length(buffer, stops):
    stops = [s for s in stops if s]
    if not stops:
        return len(buffer)
    longest = max(len(s) for s in stops)
    for k in range(min(len(buffer), longest - 1), 0, -1):
        suffix = buffer[-k:]
        if any(len(s) > k and s.startswith(suffix) for s in stops):
            return len(buffer) - k
    return len(buffer)
