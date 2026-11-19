## Statement

Same-size 2D cross-correlation with **zero padding**: $Y_{y,x} = \sum_{k_y,\,k_x} X_{\,y + k_y - \lfloor F_H/2 \rfloor,\; x + k_x - \lfloor F_W/2 \rfloor}\, F_{k_y,\,k_x}$, with out-of-range input treated as 0. `FH` and `FW` are odd.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void conv2d(const float* X, const float* F, float* Y, int H, int W, int FH, int FW)</p>

### How it is launched

2D blocks of `(16, 16)`; `x` covers columns, `y` rows. A shared-memory tile with a halo is the optimization; a direct kernel is a correct baseline.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
