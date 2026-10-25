from collections import deque


def binary_numbers_up_to(n):
    out = []
    queue = deque(["1"])
    for _ in range(n):
        front = queue.popleft()
        out.append(front)
        queue.append(front + "0")
        queue.append(front + "1")
    return out
