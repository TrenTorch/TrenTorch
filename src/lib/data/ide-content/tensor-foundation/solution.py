import numpy as np


class Tensor:
    def __init__(self, data):
        if isinstance(data, Tensor):
            self.data = data.data.astype(np.float32)
        else:
            self.data = np.asarray(data, dtype=np.float32)

    @property
    def shape(self):
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

    @property
    def size(self):
        return self.data.size

    def __repr__(self):
        return f"Tensor({self.data})"

    def add(self, other):
        other_data = other.data if isinstance(other, Tensor) else other
        return Tensor(self.data + other_data)

    def sub(self, other):
        other_data = other.data if isinstance(other, Tensor) else other
        return Tensor(self.data - other_data)

    def mul(self, other):
        other_data = other.data if isinstance(other, Tensor) else other
        return Tensor(self.data * other_data)

    def matmul(self, other):
        other_data = other.data if isinstance(other, Tensor) else other
        return Tensor(np.matmul(self.data, other_data))

    def reshape(self, *new_shape):
        if len(new_shape) == 1 and isinstance(new_shape[0], (list, tuple)):
            shape = new_shape[0]
        else:
            shape = new_shape
        return Tensor(self.data.reshape(shape))

    def transpose(self, *axes):
        if len(axes) == 0:
            return Tensor(self.data.T)
        if len(axes) == 1 and isinstance(axes[0], (list, tuple)):
            axes = axes[0]
        return Tensor(np.transpose(self.data, axes))

    def sum(self, axis=None, keepdims=False):
        return Tensor(np.sum(self.data, axis=axis, keepdims=keepdims))

    def __add__(self, other): return self.add(other)
    def __sub__(self, other): return self.sub(other)
    def __mul__(self, other): return self.mul(other)
    def __matmul__(self, other): return self.matmul(other)
