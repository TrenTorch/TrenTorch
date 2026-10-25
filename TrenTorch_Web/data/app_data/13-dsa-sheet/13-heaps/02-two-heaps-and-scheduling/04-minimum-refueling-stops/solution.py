import heapq


def min_refuel_stops(target, start_fuel, stations):
    heap = []
    reach = start_fuel
    stops = 0
    i = 0
    while reach < target:
        while i < len(stations) and stations[i][0] <= reach:
            heapq.heappush(heap, -stations[i][1])
            i += 1
        if not heap:
            return -1
        reach += -heapq.heappop(heap)
        stops += 1
    return stops
