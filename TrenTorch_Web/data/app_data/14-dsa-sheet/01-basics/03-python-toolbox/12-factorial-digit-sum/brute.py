def factorial_digit_sum(n):
    value = 1
    for i in range(2, n + 1):
        value *= i
    total = 0
    while value:
        value, chunk = divmod(value, 10**9)
        while chunk:
            chunk, digit = divmod(chunk, 10)
            total += digit
    return total
