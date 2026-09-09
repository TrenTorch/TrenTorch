# Tensor Foundation

Build a multidimensional `Tensor` class supporting arithmetic, matrix multiplication, and shape transformations, using pure NumPy underneath.

## Task

Fill in `Tensor`'s core operations:

- `add`, `sub`, `mul` -- elementwise, against another `Tensor` or a scalar.
- `matmul` -- matrix multiplication against another `Tensor`.
- `reshape` -- return a new `Tensor` with reshaped data.
- `transpose` -- permute the dimensions.
- `sum` -- reduce over an axis (or all axes).

The operator overloads (`+`, `-`, `*`, `@`) are already wired to these methods -- implement the methods and the operators work for free.

## Example

```python
>>> a = Tensor([1.0, 2.0, 3.0])
>>> b = Tensor([4.0, 5.0, 6.0])
>>> (a + b).data
array([5., 7., 9.])
```
