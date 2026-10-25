def run_browser_history(homepage, ops):
    history = [homepage]
    index = 0
    out = []
    for op in ops:
        kind, arg = op.split()
        if kind == "visit":
            del history[index + 1 :]
            history.append(arg)
            index += 1
        elif kind == "back":
            index = max(0, index - int(arg))
            out.append(history[index])
        else:
            index = min(len(history) - 1, index + int(arg))
            out.append(history[index])
    return out
