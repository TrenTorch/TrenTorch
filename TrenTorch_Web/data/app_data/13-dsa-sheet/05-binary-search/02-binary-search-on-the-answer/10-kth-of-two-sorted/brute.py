def kth_of_two_sorted(a, b, k):
    return sorted(list(a) + list(b))[k - 1]
