## Statement

Compute the leaky ReLU, where $\alpha$ is the argument `alpha`:

$$Y_i = \begin{cases} X_i & X_i \ge 0 \\ \alpha\, X_i & X_i < 0 \end{cases}$$

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void leaky_relu(const float* X, float* Y, int N, float alpha)</p>

### How it is launched

256 threads per block, $\lceil N / 256 \rceil$ blocks. `alpha` is passed by value.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

### Example

`alpha = 0.1`, `X = [-2, 0, 3]` gives `Y = [-0.2, 0, 3]`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
