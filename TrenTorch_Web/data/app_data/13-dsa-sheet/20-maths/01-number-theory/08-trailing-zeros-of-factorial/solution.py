def trailing_zeros(n):
    count = 0
    while n:
        n //= 5
        count += n
    return count
