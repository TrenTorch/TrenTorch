## Statement

Compute $C = \mathrm{ReLU}(AB + b)$ where `bias[j]` is added to every element of column `j`. Do it in **one kernel**: apply the bias and ReLU while the accumulator is still in a register, so `C` is written once instead of being re-read and re-written by two extra kernels (this is the forward pass of a `Linear` layer followed by ReLU).

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void matmul_bias_relu(const float* A, const float* B, const float* bias, float* C, int M, int N, int K)</p>

### How it is launched

2D blocks of `(16, 16)`: `x` covers columns, `y` rows. Grid $\lceil N / 16 \rceil$ by $\lceil M / 16 \rceil$.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
