def lower_bound(a: list, x) -> int:
    low, high = 0, len(a)
    while low < high:
        mid = (low + high) // 2
        if a[mid] < x:
            low = mid + 1
        else:
            high = mid
    return low


def upper_bound(a: list, x) -> int:
    low, high = 0, len(a)
    while low < high:
        mid = (low + high) // 2
        if a[mid] <= x:
            low = mid + 1
        else:
            high = mid
    return low


def range_query(a: list, low, high) -> list:
    return a[lower_bound(a, low) : upper_bound(a, high)]


def insert_sorted(a: list, x) -> list:
    position = upper_bound(a, x)
    return a[:position] + [x] + a[position:]
