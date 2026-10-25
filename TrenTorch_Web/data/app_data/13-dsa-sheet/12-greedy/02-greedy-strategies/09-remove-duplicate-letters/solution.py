def remove_duplicate_letters(s):
    last = {ch: i for i, ch in enumerate(s)}
    stack = []
    in_stack = set()
    for i, ch in enumerate(s):
        if ch in in_stack:
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            in_stack.discard(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)
