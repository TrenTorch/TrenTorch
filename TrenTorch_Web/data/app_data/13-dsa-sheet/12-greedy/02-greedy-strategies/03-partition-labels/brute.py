def partition_labels(s):
    sizes = []
    start = 0
    for i in range(1, len(s) + 1):
        if i == len(s) or not set(s[start:i]) & set(s[i:]):
            sizes.append(i - start)
            start = i
    return sizes
