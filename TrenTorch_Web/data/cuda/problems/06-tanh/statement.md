## Statement

Compute $Y_i = \tanh(X_i)$.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void tanh_kernel(const float* X, float* Y, int N)</p>

### How it is launched

256 threads per block, $\lceil N / 256 \rceil$ blocks.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Large magnitudes (±20) must give ±1, not `NaN`. Beware formulas built from `exp` that overflow.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
