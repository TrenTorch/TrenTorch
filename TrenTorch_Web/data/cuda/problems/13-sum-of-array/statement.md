## Statement

Compute $\text{out}_0 = \sum_{i=0}^{N-1} X_i$ with a **two-kernel tree reduction**. Stage 1 writes one partial result per block; stage 2 (a single block of 32 threads, so at most 32 partials) combines them.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void sum_partials(const float* X, float* partial, int N)<br>__global__ void sum_final(const float* partial, float* out, int blocks)</p>

### How it is launched

`sum_partials`: 256 threads per block, $\lceil N / 256 \rceil$ blocks, `256 * 4` bytes of **dynamic shared memory** (`extern __shared__ float s[]`). `sum_final`: one block of 32 threads and 128 bytes of dynamic shared memory.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Threads past `N` (or past `blocks`) must contribute `0`, and every thread must reach every `__syncthreads()`.
- Float addition is not associative: the checker allows a small tolerance for different summation orders.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
