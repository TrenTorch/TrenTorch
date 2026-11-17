def min_meeting_rooms(meetings):
    best = 0
    for start, _ in meetings:
        running = sum(1 for s, e in meetings if s <= start < e)
        best = max(best, running)
    return best
