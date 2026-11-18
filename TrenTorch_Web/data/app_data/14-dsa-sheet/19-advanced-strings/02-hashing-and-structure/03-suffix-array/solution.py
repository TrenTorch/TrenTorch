def suffix_array(s):
    if not s:
        return []
    text = [ord(ch) + 1 for ch in s] + [0]  # 0 is the sentinel, smaller than every letter
    n = len(text)
    size = max(max(text) + 1, n)
    order = [0] * n
    cls = [0] * n
    count = [0] * size
    for v in text:
        count[v] += 1
    for i in range(1, size):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        count[text[i]] -= 1
        order[count[text[i]]] = i
    classes = 1
    for i in range(1, n):
        if text[order[i]] != text[order[i - 1]]:
            classes += 1
        cls[order[i]] = classes - 1
    shift = 1
    while shift < n:
        by_second = [(o - shift) % n for o in order]
        count = [0] * classes
        for i in range(n):
            count[cls[by_second[i]]] += 1
        for i in range(1, classes):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            c = cls[by_second[i]]
            count[c] -= 1
            order[count[c]] = by_second[i]
        new_cls = [0] * n
        classes = 1
        for i in range(1, n):
            a, b = order[i], order[i - 1]
            if (cls[a], cls[(a + shift) % n]) != (cls[b], cls[(b + shift) % n]):
                classes += 1
            new_cls[a] = classes - 1
        new_cls[order[0]] = 0
        cls = new_cls
        shift *= 2
    return order[1:]
