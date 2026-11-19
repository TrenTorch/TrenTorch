### Stable row algorithm
1. Reduce row maximum `m`.
2. Compute `e[j] = exp(x[j]-m)` and reduce `s=sum(e)`.
3. Write `e[j]/s`.

For rows that fit efficiently in one block, assign a block per row and use warp/block reductions. For very wide rows, use a multi-block strategy or a tiled online-softmax algorithm. A naive one-block-per-row kernel may have too few blocks for a small number of huge rows.

### Online merge state
A tile can be summarized by `(m,l)`, where `m` is its max and `l=sum(exp(x-m))`. Merge states:
```text
m = max(mA,mB)
l = lA*exp(mA-m) + lB*exp(mB-m)
```
This enables streaming/tiled stable softmax without retaining all exponentials. If output probabilities are required, a final pass is still needed to write them.

### Performance
For moderate rows, softmax is often bandwidth- and reduction-latency-sensitive. For large rows, parallelism and scratch traffic matter. Avoid unstated assumptions about row width or mask semantics.
