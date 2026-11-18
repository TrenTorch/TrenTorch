def min_stack(ops):
    values = []
    out = []
    for op in ops:
        if op.startswith("push"):
            values.append(int(op.split()[1]))
        elif op == "pop":
            values.pop()
        elif op == "top":
            out.append(values[-1])
        else:
            out.append(min(values))
    return out
