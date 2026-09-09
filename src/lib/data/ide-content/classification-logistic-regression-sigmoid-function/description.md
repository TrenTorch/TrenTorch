# Sigmoid Function

Squash any real number into the (0, 1) range -- the core nonlinearity behind logistic regression.

## Task

Implement `sigmoid(x)`:

- `x` is a NumPy array of any shape.
- Return `1 / (1 + exp(-x))`, elementwise.

## Example

```python
>>> sigmoid(np.array([0.0, 2.0, -2.0]))
array([0.5, 0.8808, 0.1192])
```
