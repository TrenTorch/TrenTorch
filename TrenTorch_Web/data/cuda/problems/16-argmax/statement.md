## Statement

Return the **index** of the maximum of `X[0..N)`. When several elements tie for the maximum, return the **smallest index**.

Reduce `(value, index)` pairs: the index is part of the reduction state, so reducing only the value loses the answer.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void argmax_partials(const float* X, float* pval, int* pidx, int N)<br>__global__ void argmax_final(const float* pval, const int* pidx, int* out, int blocks)</p>

### How it is launched

`argmax_partials`: 256 threads per block, $\lceil N / 256 \rceil$ blocks; declare your own static shared arrays of 256 entries (`__shared__ float sval[256]; __shared__ int sidx[256];`). `argmax_final`: one block of 32 threads; static shared arrays of 256 entries are fine too.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Inactive threads should carry `(-INFINITY, INT_MAX)` so they never win a tie.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
