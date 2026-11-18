def monotone_increasing_digits(n):
    while True:
        text = str(n)
        if all(text[i] <= text[i + 1] for i in range(len(text) - 1)):
            return n
        n -= 1
