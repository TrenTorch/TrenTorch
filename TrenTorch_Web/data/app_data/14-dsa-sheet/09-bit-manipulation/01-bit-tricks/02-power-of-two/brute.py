def is_power_of_two(n):
    return any(n == 2**k for k in range(63))
