## Statement

Compute $Y_i = \max(X_i,\, 0)$ for every element.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void relu(const float* X, float* Y, int N)</p>

### How it is launched

256 threads per block, $\lceil N / 256 \rceil$ blocks.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

### Example

`X = [-2, 0, 3.5]` gives `Y = [0, 0, 3.5]`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
