## Statement

Row-wise softmax of a `rows x K` row-major matrix: $Y_{rj} = \dfrac{e^{X_{rj} - m}}{\sum_k e^{X_{rk} - m}}$ with $m = \max_k X_{rk}$.

Subtracting the row maximum is mandatory: some test rows contain values near 1000, where a naive `exp` overflows to infinity.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void softmax_rows(const float* X, float* Y, int rows, int K)</p>

### How it is launched

One block of **128 threads per row** (`grid = rows`). Rows can be wider than the block, so each thread loops over columns with a stride of `blockDim.x`. Declare your own static shared arrays (`__shared__ float s[128];`).

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Every thread must reach every `__syncthreads()`, including threads with no column to process.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
