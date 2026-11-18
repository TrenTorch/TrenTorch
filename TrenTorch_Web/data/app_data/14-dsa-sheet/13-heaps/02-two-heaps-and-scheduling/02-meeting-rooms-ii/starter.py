def min_meeting_rooms(meetings: list[list[int]]) -> int:
    """Return the fewest rooms that hold all the meetings."""
    # This is correct but too slow: at each start time it counts the meetings that are running.
    best = 0
    for start, _ in meetings:
        running = sum(1 for s, e in meetings if s <= start < e)
        best = max(best, running)
    return best
