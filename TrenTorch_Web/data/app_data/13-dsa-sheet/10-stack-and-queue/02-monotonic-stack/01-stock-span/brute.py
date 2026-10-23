def stock_span(prices):
    out = []
    for i in range(len(prices)):
        span = 1
        while i - span >= 0 and prices[i - span] <= prices[i]:
            span += 1
        out.append(span)
    return out
