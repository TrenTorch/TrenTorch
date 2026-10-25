from collections import deque


def min_jumps(nums):
    n = len(nums)
    if n <= 1:
        return 0
    dist = {0: 0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if j not in dist:
                dist[j] = dist[i] + 1
                queue.append(j)
    return dist.get(n - 1, -1)
