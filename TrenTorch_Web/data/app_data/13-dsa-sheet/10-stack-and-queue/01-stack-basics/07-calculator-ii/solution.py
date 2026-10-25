def calculate(s):
    stack = []
    num = 0
    op = "+"
    for i, ch in enumerate(s + "+"):
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch != " ":
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                top = stack.pop()
                q = abs(top) // num
                stack.append(q if top >= 0 else -q)
            op = ch
            num = 0
    return sum(stack)
