import sys


def multiply_strings(a, b):
    sys.set_int_max_str_digits(0)
    return str(int(a) * int(b))
