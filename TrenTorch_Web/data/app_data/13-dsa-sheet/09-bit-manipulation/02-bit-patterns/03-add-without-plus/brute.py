def bit_add(a, b):
    return (a + b + 2**31) % 2**32 - 2**31
