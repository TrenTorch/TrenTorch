### Definitions
Population mean: `mu = sum(x)/N`. Population variance: `sum((x-mu)^2)/N`. Sample variance instead divides by `N-1`; state which one is required.

### Options
1. **Two-pass:** reduce sum to obtain mean, then reduce squared deviations. Stable and simple, but reads the input twice.
2. **Raw moments:** compute `E[x²] - E[x]²` in one pass. Less traffic but can suffer catastrophic cancellation when variance is small relative to the mean.
3. **Welford:** merge `(count, mean, M2)` tuples. More arithmetic/state, but numerically robust and parallelizable.

### Welford merge
For summaries `a=(na,ma,M2a)` and `b=(nb,mb,M2b)`:
```text
n = na + nb
delta = mb - ma
mean = ma + delta * nb / n
M2 = M2a + M2b + delta*delta * na*nb/n
```
Use a tested pairwise block reduction over these tuples. Return `M2/N` for population variance or `M2/(N-1)` for sample variance.

### Optimality discussion
The two-pass method is often attractive when accuracy matters and memory bandwidth is available. Welford reduces multiple partial summaries and avoids a second input read, but has higher per-element arithmetic and more complex reduction state. Benchmark for the actual distribution and tolerance.
