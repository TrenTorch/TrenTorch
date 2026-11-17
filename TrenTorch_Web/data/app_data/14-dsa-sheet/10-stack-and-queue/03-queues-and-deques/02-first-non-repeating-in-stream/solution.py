from collections import deque


def first_non_repeating_stream(s):
    counts = {}
    queue = deque()
    out = []
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
        if counts[ch] == 1:
            queue.append(ch)
        while queue and counts[queue[0]] > 1:
            queue.popleft()
        out.append(queue[0] if queue else "#")
    return "".join(out)
