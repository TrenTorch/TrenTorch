# Mean Squared Error

Implement MSE, the default loss for regression.

## Task

Implement `mse_loss(y_pred, y_true)`:

- `y_pred` and `y_true` are NumPy arrays of the same shape.
- Return a single scalar: the mean of the squared elementwise differences.

## Example

```python
>>> mse_loss(np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 5.0]))
1.3333333333333333
```
