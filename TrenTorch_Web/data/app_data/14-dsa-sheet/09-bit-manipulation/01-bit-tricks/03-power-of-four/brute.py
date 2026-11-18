def is_power_of_four(n):
    return any(n == 4**k for k in range(32))
