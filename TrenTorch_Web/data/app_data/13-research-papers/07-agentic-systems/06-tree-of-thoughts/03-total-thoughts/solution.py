def total_thoughts(b, depth):
    return sum(b**t for t in range(1, depth + 1))
