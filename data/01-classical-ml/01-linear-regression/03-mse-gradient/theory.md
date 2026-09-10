We can now make predictions and measure their error.

But we still have a problem:

How do we change `w` and `b` so that the loss becomes smaller?

This is where the gradient comes in.

The gradient tells us how the loss changes when we change the parameters.

For MSE, the gradients are:

```text
dL/dw = (2/n) Xᵀ(ŷ - y)
dL/db = (2/n) Σ(ŷ - y)
```

So:

- `dw` tells us how each weight affects the loss.
- `db` tells us how the bias affects the loss.

This gives us the missing connection:

```text
X, w, b
   ↓
prediction
   ↓
loss
   ↓
gradient
   ↓
how should w and b change?
```

For this track, you will calculate these derivatives manually rather than using automatic differentiation.
