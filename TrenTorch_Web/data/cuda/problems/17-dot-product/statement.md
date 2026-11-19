## Statement

Compute $\text{out}_0 = \sum_{i=0}^{N-1} A_i B_i$. The first kernel uses a **grid-stride loop**, so a fixed number of blocks can cover any `N`; each thread accumulates privately, then the block reduces. A second kernel combines the per-block partials.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void dot_partials(const float* A, const float* B, float* partial, int N)<br>__global__ void dot_final(const float* partial, float* out, int blocks)</p>

### How it is launched

`dot_partials`: exactly **8 blocks of 256 threads** (fewer threads than elements) and `256 * 4` bytes dynamic shared memory. `dot_final`: one block of 32 threads, 128 bytes dynamic shared memory, `blocks = 8`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Because the grid is smaller than `N`, a thread must process several elements with `i += blockDim.x * gridDim.x`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
