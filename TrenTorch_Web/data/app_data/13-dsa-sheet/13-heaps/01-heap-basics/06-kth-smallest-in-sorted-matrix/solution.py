import heapq


def kth_smallest_matrix(matrix, k):
    heap = [(matrix[r][0], r, 0) for r in range(len(matrix))]
    heapq.heapify(heap)
    for _ in range(k - 1):
        _, r, c = heapq.heappop(heap)
        if c + 1 < len(matrix[r]):
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
    return heap[0][0]
