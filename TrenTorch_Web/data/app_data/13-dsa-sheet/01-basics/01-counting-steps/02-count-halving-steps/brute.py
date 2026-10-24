def count_halving_steps(n):
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count
