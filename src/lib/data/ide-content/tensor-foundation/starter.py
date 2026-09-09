import numpy as np


class Tensor:
    """
    Multidimensional array container for TrenTorch operations.
    """
    def __init__(self, data):
        # Convert input data to a numpy float32 ndarray
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
        """Element-wise addition with another Tensor or scalar."""
        # TODO: Implement element-wise addition
        pass

    def sub(self, other):
        """Element-wise subtraction with another Tensor or scalar."""
        # TODO: Implement element-wise subtraction
        pass

    def mul(self, other):
        """Element-wise multiplication with another Tensor or scalar."""
        # TODO: Implement element-wise multiplication
        pass

    def matmul(self, other):
        """Matrix multiplication between self and other."""
        # TODO: Implement matrix multiplication
        pass

    def reshape(self, *new_shape):
        """Returns a new Tensor with reshaped data."""
        # TODO: Implement reshape
        pass

    def transpose(self, *axes):
        """Permute the dimensions of the Tensor."""
        # TODO: Implement transpose
        pass

    def sum(self, axis=None, keepdims=False):
        """Sum array elements over a given axis."""
        # TODO: Implement sum
        pass

    # Operator Overloads
    def __add__(self, other): return self.add(other)
    def __sub__(self, other): return self.sub(other)
    def __mul__(self, other): return self.mul(other)
    def __matmul__(self, other): return self.matmul(other)
