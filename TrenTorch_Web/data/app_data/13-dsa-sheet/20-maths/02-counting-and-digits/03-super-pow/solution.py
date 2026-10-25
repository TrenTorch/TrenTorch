def super_pow(a, b):
    result = 1
    for digit in b:
        result = pow(result, 10, 1337) * pow(a, digit, 1337) % 1337
    return result
