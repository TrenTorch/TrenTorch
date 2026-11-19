## Statement

Given `a[M]` and `b[N]`, produce the `M x N` row-major matrix $C_{ij} = a_i\, b_j$.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void outer_product(const float* a, const float* b, float* C, int M, int N)</p>

### How it is launched

2D blocks of `(16, 16)`: `x` covers columns `j` (0..N), `y` covers rows `i` (0..M).

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
