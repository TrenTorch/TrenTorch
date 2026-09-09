# ReLU: Forward + Backward

Implement ReLU's forward pass and its gradient.

## Forward

Implement `relu_forward(x)`: return `max(0, x)`, elementwise.

## Backward

Implement `relu_backward(grad_output, x)`, where `grad_output` is the gradient arriving from the next layer and `x` is the original input to the forward pass. Pass the gradient through only where `x` was positive.

## Example

```python
>>> relu_forward(np.array([-2.0, 0.0, 3.0]))
array([0.0, 0.0, 3.0])

>>> relu_backward(np.array([1.0, 1.0, 1.0]), np.array([-2.0, 0.0, 3.0]))
array([0.0, 0.0, 1.0])
```
