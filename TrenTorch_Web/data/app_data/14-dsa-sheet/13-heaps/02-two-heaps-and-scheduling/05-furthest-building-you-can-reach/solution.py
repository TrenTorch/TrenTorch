import heapq


def furthest_building(heights, bricks, ladders):
    heap = []
    for i in range(1, len(heights)):
        climb = heights[i] - heights[i - 1]
        if climb <= 0:
            continue
        heapq.heappush(heap, climb)
        if len(heap) > ladders:
            bricks -= heapq.heappop(heap)
            if bricks < 0:
                return i - 1
    return len(heights) - 1
