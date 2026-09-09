We now know the direction in which the loss increases.

To reduce the loss, we move in the opposite direction.

This is gradient descent:

```text
w = w - lr * dw
b = b - lr * db
```

where `lr` is the learning rate.

The learning rate controls how large a step we take:

- too small → learning is very slow;
- too large → we may overshoot or become unstable.

One update gives us one step toward better parameters.

So the complete idea so far is:

```text
1. Make predictions
2. Calculate loss
3. Calculate gradients
4. Update parameters
```
