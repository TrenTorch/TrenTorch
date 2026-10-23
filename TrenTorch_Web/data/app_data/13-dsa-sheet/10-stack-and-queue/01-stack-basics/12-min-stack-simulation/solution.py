def min_stack(ops):
    values = []
    mins = []
    out = []
    for op in ops:
        if op.startswith("push"):
            x = int(op.split()[1])
            values.append(x)
            mins.append(min(x, mins[-1]) if mins else x)
        elif op == "pop":
            values.pop()
            mins.pop()
        elif op == "top":
            out.append(values[-1])
        else:
            out.append(mins[-1])
    return out
