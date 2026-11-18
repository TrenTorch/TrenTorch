import heapq


def min_meeting_rooms(meetings):
    rooms = []
    for start, end in sorted(meetings):
        if rooms and rooms[0] <= start:
            heapq.heapreplace(rooms, end)
        else:
            heapq.heappush(rooms, end)
    return len(rooms)
