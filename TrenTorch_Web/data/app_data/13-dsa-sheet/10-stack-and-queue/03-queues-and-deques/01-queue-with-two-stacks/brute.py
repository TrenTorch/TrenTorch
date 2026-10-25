from collections import deque


def queue_with_two_stacks(ops):
    q = deque()
    out = []
    for op in ops:
        if op.startswith("push"):
            q.append(int(op.split()[1]))
        elif op == "pop":
            out.append(q.popleft())
        elif op == "peek":
            out.append(q[0])
        else:
            out.append(0 if q else 1)
    return out
