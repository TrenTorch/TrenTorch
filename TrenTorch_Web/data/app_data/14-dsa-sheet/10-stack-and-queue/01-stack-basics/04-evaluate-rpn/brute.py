def evaluate_rpn(tokens):
    tokens = list(tokens)
    while len(tokens) > 1:
        i = next(k for k, t in enumerate(tokens) if t in ("+", "-", "*", "/"))
        a, b = int(tokens[i - 2]), int(tokens[i - 1])
        if tokens[i] == "+":
            value = a + b
        elif tokens[i] == "-":
            value = a - b
        elif tokens[i] == "*":
            value = a * b
        else:
            q = abs(a) // abs(b)
            value = q if (a < 0) == (b < 0) else -q
        tokens[i - 2 : i + 1] = [str(value)]
    return int(tokens[0])
