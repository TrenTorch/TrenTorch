`error = y_hat - y` is computed once and reused for both `dw` and `db`, instead of recomputing the subtraction twice.

`X.T @ error`, not `error @ X.T` — get this backwards and `dw` comes out with the _wrong shape entirely_ rather than a subtly wrong value, which is why a dedicated shape test exists separate from the numeric ones.

`db` gets the same `float(...)` treatment as `mse_loss`, for the same reason: `np.sum` returns a NumPy scalar, not a Python float.
