from collections import deque


def num_squares(n):
    if n == 0:
        return 0
    seen = {0}
    queue = deque([(0, 0)])
    while queue:
        total, used = queue.popleft()
        k = 1
        while total + k * k <= n:
            nxt = total + k * k
            if nxt == n:
                return used + 1
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, used + 1))
            k += 1
    return 0
