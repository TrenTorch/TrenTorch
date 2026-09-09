A model needs a rule for turning inputs into predictions.

In linear regression, that rule is:

```text
ŷ = Xw + b
```

Here:

- `X` contains the input features.
- `w` contains one weight for each feature.
- `b` is the bias.
- `ŷ` is the prediction made by the model.

For one example with two features:

```text
ŷ = x₁w₁ + x₂w₂ + b
```

For many examples, matrix multiplication lets us calculate all predictions at once:

```text
ŷ = X @ w + b
```

This equation is called the hypothesis function.

Important: at this point, we are only defining what the model can represent. We have not learned the values of `w` and `b` yet.
