The gradient of BCE with respect to the raw linear score `z` simplifies to exactly:

```text
dL/dz = p - y
dw = (1/n) X.T @ (p - y)
db = (1/n) sum(p - y)
```

The same "prediction minus target" shape as Linear Regression's residual, built on top of a different upstream function.
