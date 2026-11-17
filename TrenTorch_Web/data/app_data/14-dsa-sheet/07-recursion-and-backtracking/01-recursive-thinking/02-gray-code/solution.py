def gray_code(n):
    return [i ^ (i >> 1) for i in range(2**n)]
