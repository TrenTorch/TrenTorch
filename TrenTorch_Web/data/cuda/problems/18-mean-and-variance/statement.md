## Statement

Compute the **mean** and the **population variance** $\dfrac{1}{N}\sum_i (x_i - \mu)^2$ of `X[0..N)` and store them in `out[0]` and `out[1]`.

The data have a large offset (around 10,000) with a small spread, so the shortcut `E[x²] - E[x]²` loses all its digits to cancellation. Use a two-pass approach (mean first, then squared deviations) or a Welford merge.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void mean_var(const float* X, float* out, int N)</p>

### How it is launched

A **single block of 256 threads** handles the whole array ($N \le 4096$), so use a loop `for (i = threadIdx.x; i < N; i += blockDim.x)`. Declare your own static shared arrays of 256 floats.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Reading `X` twice is fine; the lesson is stability, not minimum traffic.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
