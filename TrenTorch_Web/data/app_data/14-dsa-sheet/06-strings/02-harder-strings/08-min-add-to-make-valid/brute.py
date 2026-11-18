def min_add_to_make_valid(s):
    stack = []
    for ch in s:
        if ch == ")" and stack and stack[-1] == "(":
            stack.pop()
        else:
            stack.append(ch)
    return len(stack)
