## Statement

Compute the exact GELU $Y_i = 0.5\,x\left(1 + \operatorname{erf}\!\left(\dfrac{x}{\sqrt{2}}\right)\right)$ with `x = X[i]`.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void gelu_exact(const float* X, float* Y, int N)</p>

### How it is launched

256 threads per block, $\lceil N / 256 \rceil$ blocks.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Use `erff`. The tanh approximation is a different function and is rejected by the tolerance.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
