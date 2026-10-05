import math


class Vector:
    def __init__(self, buffer, indices=None):
        self.buffer = buffer
        self.indices = indices if indices is not None else range(len(buffer))

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Vector(self.buffer, self.indices[key])
        return self.buffer[self.indices[key]]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            positions = self.indices[key]
            if hasattr(value, "__len__"):
                snapshot = list(value)
                if len(snapshot) != len(positions):
                    raise ValueError("length mismatch")
                for pos, v in zip(positions, snapshot):
                    self.buffer[pos] = v
            else:
                for pos in positions:
                    self.buffer[pos] = value
        else:
            self.buffer[self.indices[key]] = value

    def to_list(self):
        return [self.buffer[i] for i in self.indices]

    def copy(self):
        return Vector(self.to_list())

    def map(self, func):
        return Vector([func(x) for x in self.to_list()])

    def __add__(self, other):
        if hasattr(other, "__len__"):
            return Vector([a + b for a, b in zip(self.to_list(), list(other))])
        return Vector([x + other for x in self.to_list()])

    def __radd__(self, other):
        return self + other

    def normalize_(self, eps=1e-5):
        values = self.to_list()
        n = len(values)
        if n == 0:
            return self
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / n
        denom = math.sqrt(variance + eps)
        for value, pos in zip(values, self.indices):
            self.buffer[pos] = (value - mean) / denom
        return self

    def __repr__(self):
        return f"Vector({self.to_list()!r})"
