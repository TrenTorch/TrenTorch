## Statement

For every row compute $\mathrm{softmax}(s\,X + \text{mask})$ where a **masked** position (`mask[r][j] == 0`) is excluded: it gets probability `0` and takes no part in the maximum or the sum. Do scale, mask, max, sum and normalise inside **one kernel** so no intermediate row is written to memory.

If a whole row is masked, write all zeros (not `NaN` from `-inf - -inf`).

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void fused_scale_mask_softmax(const float* X, const int* mask, float* Y, int rows, int K, float scale)</p>

### How it is launched

One block of **128 threads per row** (`grid = rows`); rows can be wider than the block. Declare a static `__shared__ float s[128];`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- `mask` holds `1` for keep and `0` for masked, laid out like `X`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
