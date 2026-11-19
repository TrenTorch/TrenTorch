## Statement

This kernel loads `valid` elements into shared memory and writes them back reversed, with zero for positions that have no data: `out[t] = (63 - t < valid) ? in[63 - t] : 0`. It works when `valid = 64` but hangs (or is undefined behaviour on real hardware) when some threads are inactive, because `__syncthreads()` sits inside a branch. Fix it.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void reverse_valid(const float* in, float* out, int valid)</p>

### How it is launched

One block of 64 threads. `valid` is between 1 and 64.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Every thread of the block must reach the same `__syncthreads()`. Give inactive lanes a neutral value (`0`) instead of skipping the barrier.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
