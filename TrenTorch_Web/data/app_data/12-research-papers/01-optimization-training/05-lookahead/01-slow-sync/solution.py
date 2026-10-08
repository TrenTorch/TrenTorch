def lookahead_sync(slow, fast, alpha):
    return slow + alpha * (fast - slow)
