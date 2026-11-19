### Stable formulation
`m=max(z)`, then:
`loss = m + log(sum(exp(z[k]-m))) - z[t]`.

### Kernel structure
One block per row for moderate class counts:
1. Reduce max.
2. Reduce exponentials relative to max.
3. Read target logit and write one loss per row.
For very large `K`, use tiled/online log-sum-exp state. For label smoothing or probability targets, the loss definition changes and must be specified.

### Numerical and performance notes
Never compute `log(sum(exp(z)))` directly for arbitrary logits. The stable max subtraction prevents overflow. This operation reads logits and writes one scalar per row, so reduction and launch overhead can be important for small batches.

---
