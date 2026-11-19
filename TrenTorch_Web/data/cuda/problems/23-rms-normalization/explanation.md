### Kernel structure
Each block handles one row. Threads accumulate squared values across columns, reduce the sum, compute `inv_rms = rsqrt(sum/K + eps)`, then normalize and optionally multiply by `weight[j]`.

### Design notes
- Ensure all threads reach every `__syncthreads()`; use neutral values for masked columns.
- For widths larger than one block can handle efficiently, use multiple warps per row or a multi-stage method.
- Epsilon placement is part of the operator definition.
- Fuse scale/weight and any compatible activation into the epilogue to avoid extra memory passes.
