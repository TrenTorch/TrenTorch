def decode_string(s):
    out = []
    open_blocks = []
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            open_blocks.append((len(out), num))
            num = 0
        elif ch == "]":
            start, count = open_blocks.pop()
            if count == 0:
                del out[start:]
            elif count > 1:
                out.extend(out[start:] * (count - 1))
        else:
            out.append(ch)
    return "".join(out)
