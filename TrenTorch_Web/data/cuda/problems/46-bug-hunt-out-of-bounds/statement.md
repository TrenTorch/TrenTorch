## Statement

This kernel should double every element, $Y_i = 2 X_i$, but it reads and writes past the end of the arrays whenever `N` is not a multiple of the block size. Fix it without changing the signature.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void double_it(const float* X, float* Y, int N)</p>

### How it is launched

256 threads per block and $\lceil N / 256 \rceil$ blocks, so some threads always have $i \ge N$.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- The failure message names the kernel, block and thread that went out of bounds.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
