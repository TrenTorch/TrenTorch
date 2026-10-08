def skipgram_pairs(tokens, window):
    n = len(tokens)
    pairs = []
    for i in range(n):
        for j in range(max(0, i - window), min(n, i + window + 1)):
            if j != i:
                pairs.append((tokens[i], tokens[j]))
    return pairs
