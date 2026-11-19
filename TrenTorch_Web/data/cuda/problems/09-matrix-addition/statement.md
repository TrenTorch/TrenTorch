## Statement

Add two row-major matrices `A` and `B` of shape `H x W` into `C`.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void matrix_add(const float* A, const float* B, float* C, int H, int W)</p>

### How it is launched

A 2D launch with blocks of `(32, 8)` threads: `x` covers columns, `y` covers rows. The grid has $\lceil W / 32 \rceil$ by $\lceil H / 8 \rceil$ blocks.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Neighbouring lanes (`threadIdx.x`) must touch neighbouring addresses; the report shows your coalescing efficiency.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
