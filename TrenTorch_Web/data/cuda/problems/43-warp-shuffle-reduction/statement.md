## Statement

Sum 32 values held by the 32 lanes of a warp **without shared memory**, using `__shfl_down_sync`. Each block is exactly one warp (32 threads) and reduces its own 32 elements `x[32*b .. 32*b+31]`; lane 0 writes the sum to `out[b]`. Lanes whose element is past `N` contribute 0.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void warp_sum_kernel(const float* X, float* out, int N)</p>

### How it is launched

32 threads per block, $\lceil N / 32 \rceil$ blocks.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Submit checks that the kernel used **no shared memory at all**.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
