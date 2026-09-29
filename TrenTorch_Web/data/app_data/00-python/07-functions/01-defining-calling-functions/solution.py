def square(x):
    return x * x


def min_max(values):
    minimum = values[0]
    maximum = values[0]
    for value in values:
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value
    return (minimum, maximum)


def describe_pair(a, b):
    return (a + b, a - b, a * b)


def absolute_value(x):
    if x < 0:
        return -x
    return x
