def run_browser_history(homepage, ops):
    back = []
    current = homepage
    forward = []
    out = []
    for op in ops:
        kind, arg = op.split()
        if kind == "visit":
            back.append(current)
            current = arg
            forward = []
        elif kind == "back":
            for _ in range(int(arg)):
                if back:
                    forward.append(current)
                    current = back.pop()
            out.append(current)
        else:
            for _ in range(int(arg)):
                if forward:
                    back.append(current)
                    current = forward.pop()
            out.append(current)
    return out
