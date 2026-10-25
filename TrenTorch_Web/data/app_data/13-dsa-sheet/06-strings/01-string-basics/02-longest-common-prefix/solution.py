def longest_common_prefix(words):
    if not words:
        return ""
    first, last = min(words), max(words)
    i = 0
    while i < len(first) and i < len(last) and first[i] == last[i]:
        i += 1
    return first[:i]
