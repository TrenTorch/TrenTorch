def stock_span(prices: list[int]) -> list[int]:
    """For each day, return how many consecutive days up to it had a price not above it."""
    # This is correct but too slow: it walks back from every day.
    out = []
    for i in range(len(prices)):
        span = 1
        while i - span >= 0 and prices[i - span] <= prices[i]:
            span += 1
        out.append(span)
    return out
