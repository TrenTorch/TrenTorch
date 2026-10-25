from collections import deque


def run_hit_counter(ops):
    window = deque()
    out = []
    for op in ops:
        kind, t = op.split()
        t = int(t)
        if kind == "hit":
            window.append(t)
        else:
            while window and window[0] <= t - 300:
                window.popleft()
            out.append(len(window))
    return out
