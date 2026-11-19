### Baseline pipeline
1. GEMM for `QKᵀ`.
2. Row-wise stable softmax.
3. GEMM for probabilities times `V`.

This is easy to validate but writes and rereads the attention matrix.

### Fused tiled strategy
A FlashAttention-style algorithm tiles keys/values and maintains per-query-row running state `(m,l,o)`:
- `m`: running maximum score.
- `l`: running normalization sum.
- `o`: running weighted-value accumulator.
When a new score tile arrives, rescale prior `l` and `o` to the new maximum, incorporate the tile's exponentials and weighted values, and continue. Normalize `o/l` at the end.

### Why it matters
The fused method avoids materializing the full `QKᵀ`/probability matrix in global memory, reducing high-volume memory traffic. It is substantially more complex and requires careful masking, causal boundaries, numerical stability, and tile scheduling. Use a proven implementation as a correctness/performance reference.
