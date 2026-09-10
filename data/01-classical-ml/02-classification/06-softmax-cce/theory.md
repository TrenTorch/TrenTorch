```text
softmax(z)_i = exp(z_i) / Σ_j exp(z_j)
L = -log(p_correct_class)
```

With `K=2` classes, softmax + CCE reduces mathematically to sigmoid + BCE — the same idea generalized.
