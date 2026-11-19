## Statement

Compute $y_i = \dfrac{x_i}{\sqrt{\sum_j x_j^2}}$: reduce the sum of squares, then scale every element by `rsqrtf` of it.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void sumsq_partials(const float* x, float* partial, int n)<br>__global__ void sum_final(const float* partial, float* out, int blocks)<br>__global__ void l2_map(const float* x, float* y, int n, const float* sumsq)</p>

### How it is launched

`sumsq_partials`: 256 threads per block, $\lceil n / 256 \rceil$ blocks, `256 * 4` bytes dynamic shared memory. `sum_final`: one block of 32 threads and 128 bytes dynamic shared memory. `l2_map`: 256 threads per block, $\lceil n / 256 \rceil$ blocks.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
