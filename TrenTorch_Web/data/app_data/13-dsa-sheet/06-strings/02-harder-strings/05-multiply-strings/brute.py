def multiply_strings(a, b):
    result = [0] * (len(a) + len(b))
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            total = int(a[i]) * int(b[j]) + result[i + j + 1]
            result[i + j + 1] = total % 10
            result[i + j] += total // 10
    text = "".join(map(str, result)).lstrip("0")
    return text or "0"
