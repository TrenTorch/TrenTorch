import heapq


def median_sliding_window(nums, k):
    small = []  # max-heap of the lower half (stored negated)
    large = []  # min-heap of the upper half
    delayed = {}  # value -> copies that left the window but are still inside a heap
    size = [0, 0]  # live sizes of small and large

    def clean(heap, negated):
        while heap:
            value = -heap[0] if negated else heap[0]
            if delayed.get(value, 0):
                delayed[value] -= 1
                heapq.heappop(heap)
            else:
                break

    def balance():
        if size[0] > size[1] + 1:
            heapq.heappush(large, -heapq.heappop(small))
            size[0] -= 1
            size[1] += 1
            clean(small, True)
        elif size[0] < size[1]:
            heapq.heappush(small, -heapq.heappop(large))
            size[1] -= 1
            size[0] += 1
            clean(large, False)

    def add(x):
        if not small or x <= -small[0]:
            heapq.heappush(small, -x)
            size[0] += 1
        else:
            heapq.heappush(large, x)
            size[1] += 1
        balance()

    def remove(x):
        delayed[x] = delayed.get(x, 0) + 1
        if x <= -small[0]:
            size[0] -= 1
            if x == -small[0]:
                clean(small, True)
        else:
            size[1] -= 1
            if x == large[0]:
                clean(large, False)
        balance()

    def median():
        if k % 2:
            return float(-small[0])
        return (-small[0] + large[0]) / 2

    for x in nums[:k]:
        add(x)
    out = [median()]
    for i in range(k, len(nums)):
        add(nums[i])
        remove(nums[i - k])
        out.append(median())
    return out
