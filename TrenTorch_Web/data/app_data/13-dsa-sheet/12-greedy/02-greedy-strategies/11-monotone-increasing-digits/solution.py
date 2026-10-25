def monotone_increasing_digits(n):
    digits = list(str(n))
    mark = len(digits)
    for i in range(len(digits) - 1, 0, -1):
        if digits[i - 1] > digits[i]:
            digits[i - 1] = str(int(digits[i - 1]) - 1)
            mark = i
    for i in range(mark, len(digits)):
        digits[i] = "9"
    return int("".join(digits))
