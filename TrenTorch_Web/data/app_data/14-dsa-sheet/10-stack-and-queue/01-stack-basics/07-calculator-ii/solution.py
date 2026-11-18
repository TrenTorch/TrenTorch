def calculate(s):
    total = last = num = 0
    op = "+"
    for ch in s + "+":
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch != " ":
            if op == "+":
                total += last
                last = num
            elif op == "-":
                total += last
                last = -num
            elif op == "*":
                last *= num
            else:
                q = abs(last) // num
                last = q if last >= 0 else -q
            op = ch
            num = 0
    return total + last
