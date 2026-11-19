## Statement

Compute $\text{out}_0 = \min_{0 \le i < N} X_i$ with the two-kernel reduction, using `fminf`. Stage 1 writes one partial result per block; stage 2 (a single block of 32 threads, so at most 32 partials) combines them.

The identity element for min is the opposite of the one for max. All values in the hidden tests are positive.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void min_partials(const float* X, float* partial, int N)<br>__global__ void min_final(const float* partial, float* out, int blocks)</p>

### How it is launched

`min_partials`: 256 threads per block, $\lceil N / 256 \rceil$ blocks, `256 * 4` bytes dynamic shared memory. `min_final`: one block of 32 threads, 128 bytes dynamic shared memory.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
