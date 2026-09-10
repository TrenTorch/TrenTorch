So far, the model only cares about fitting the training data.

Sometimes we also want to discourage the model from using very large weights.

We can do that by adding a penalty to the objective:

```text
L_ridge = MSE + λ Σw²
```

where `λ` controls how strongly large weights are penalized.

The corresponding gradient becomes:

```text
dw_ridge = dw_mse + 2λw
db_ridge = db_mse
```

The bias is not regularized.

```text
larger λ
   ↓
stronger penalty on large weights
   ↓
smaller learned weights
```

This is called L2 regularization or weight decay in this setting.
