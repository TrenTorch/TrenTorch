## Statement

Same-size 1D cross-correlation with **zero padding**: $y_i = \sum_{k=-R}^{R} x_{i+k}\, w_{k+R}$, where `x[j] = 0` for `j < 0` or `j >= N`.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void conv1d(const float* x, const float* w, float* y, int N, int R)</p>

### How it is launched

256 threads per block, $\lceil N / 256 \rceil$ blocks. The filter `w` has $2R + 1$ entries.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Neighbours across a block boundary belong to the neighbouring block: read them from global memory (or load a halo into shared memory).

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
