The model can now make predictions, but we need a way to answer:

"How wrong are these predictions?"

That is the job of a loss function.

For linear regression, we use Mean Squared Error (MSE):

```text
L = mean((ŷ - y)²)
```

where:

- `ŷ` = predictions;
- `y` = true targets;
- `ŷ - y` = prediction error.

We square each error so that positive and negative errors do not cancel out, and large errors are penalized more strongly.

So the process is now:

```text
X → linear model → ŷ → compare with y → loss
```

The loss is a single number telling us how well the current values of `w` and `b` are performing.
