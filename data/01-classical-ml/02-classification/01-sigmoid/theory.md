Linear Regression's hypothesis, `Xw + b`, can output any real number. A probability has to live strictly between 0 and 1.

```text
sigmoid(z) = 1 / (1 + exp(-z))
z (any real number) → sigmoid → probability between 0 and 1
```

- very negative `z` → probability near 0
- very positive `z` → probability near 1
- `z = 0` → probability exactly 0.5
