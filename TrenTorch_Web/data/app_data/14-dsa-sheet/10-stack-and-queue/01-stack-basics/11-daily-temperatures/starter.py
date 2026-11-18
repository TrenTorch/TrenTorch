def daily_temperatures(temps: list[int]) -> list[int]:
    """For each day, return how many days until a warmer day (0 if never)."""
    # This is correct but too slow: it looks ahead from every day.
    out = []
    for i in range(len(temps)):
        wait = 0
        for j in range(i + 1, len(temps)):
            if temps[j] > temps[i]:
                wait = j - i
                break
        out.append(wait)
    return out
