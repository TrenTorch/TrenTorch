def happy_number(n):
    def step(x):
        total = 0
        while x:
            x, digit = divmod(x, 10)
            total += digit * digit
        return total

    slow, fast = n, step(n)
    while fast != 1 and slow != fast:
        slow = step(slow)
        fast = step(step(fast))
    return fast == 1
