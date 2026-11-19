## Statement

Same-size 3D cross-correlation with **zero padding** over a volume `D x H x W` (depth, height, width; `x` is the fastest axis) and a `KD x KH x KW` filter (all odd): `Y[z][y][x] = sum X[z + kz - KD/2][y + ky - KH/2][x + kx - KW/2] * F[kz][ky][kx]`.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void conv3d(const float* X, const float* F, float* Y, int D, int H, int W, int KD, int KH, int KW)</p>

### How it is launched

3D blocks of `(8, 4, 4)` threads; `x` covers width, `y` height, `z` depth.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Index `X[(z * H + y) * W + x]` and keep `x` as the contiguous axis.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
