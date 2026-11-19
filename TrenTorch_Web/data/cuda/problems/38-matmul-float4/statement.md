## Statement

Compute $C = AB$ where **each thread produces four consecutive outputs** `C[row][4*c .. 4*c+3]` and reads the matching four entries of `B[k][...]` with one 128-bit `float4` load, then writes the four results with one `float4` store.

`N` and `K` are multiples of 4, so every row of `B` and `C` starts on a 16-byte boundary.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void matmul_vec4(const float* A, const float* B, float* C, int M, int N, int K)</p>

### How it is launched

2D blocks of `(16, 16)` threads. `x` indexes groups of four columns (so `N / 4` of them), `y` indexes rows. Grid $\lceil (N/4) / 16 \rceil$ by $\lceil M / 16 \rceil$.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Submit checks that loads are really vectorized (average bytes per load instruction well above 4).

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
