class Accumulator:
    def __init__(self):
        self.total = 0

    def add(self, x):
        self.total = self.total + x
        return self

    def value(self):
        return self.total


def add_via_class(acc, x):
    return Accumulator.add(acc, x)


def bound_method_target(method):
    return method.__self__


def chain_adds(acc, numbers: list):
    for number in numbers:
        acc.add(number)
    return acc
