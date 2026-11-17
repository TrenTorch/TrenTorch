import math
import sys


def factorial_digit_sum(n):
    sys.set_int_max_str_digits(0)
    return sum(map(int, str(math.factorial(n))))
