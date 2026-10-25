def decode_string(s):
    stack = []
    text = ""
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            stack.append((text, num))
            text, num = "", 0
        elif ch == "]":
            saved, count = stack.pop()
            text = saved + text * count
        else:
            text += ch
    return text
