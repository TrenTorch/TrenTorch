## Statement

Compute $C = AB$ for row-major `A[M][K]`, `B[K][N]`, `C[M][N]` with one thread per output element. This is the baseline that the rest of the matmul ladder improves on: every output reads `2K` values with no reuse.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void matmul_naive(const float* A, const float* B, float* C, int M, int N, int K)</p>

### How it is launched

2D blocks of `(16, 16)`: `x` covers columns of `C`, `y` rows. Grid $\lceil N / 16 \rceil$ by $\lceil M / 16 \rceil$.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
