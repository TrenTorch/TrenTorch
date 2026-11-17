def min_platforms(arrivals, departures):
    arr = sorted(arrivals)
    dep = sorted(departures)
    current = best = 0
    i = j = 0
    while i < len(arr):
        if arr[i] <= dep[j]:
            current += 1
            best = max(best, current)
            i += 1
        else:
            current -= 1
            j += 1
    return best
