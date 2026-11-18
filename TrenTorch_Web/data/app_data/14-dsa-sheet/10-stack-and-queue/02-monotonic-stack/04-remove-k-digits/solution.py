def remove_k_digits(num, k):
    stack = []
    for ch in num:
        while k and stack and stack[-1] > ch:
            stack.pop()
            k -= 1
        stack.append(ch)
    if k:
        stack = stack[:-k]
    return "".join(stack).lstrip("0") or "0"
