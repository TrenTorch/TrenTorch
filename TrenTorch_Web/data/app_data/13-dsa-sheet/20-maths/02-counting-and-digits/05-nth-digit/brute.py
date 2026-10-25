def nth_digit(n):
    text = ""
    k = 1
    while len(text) < n:
        text += str(k)
        k += 1
    return int(text[n - 1])
