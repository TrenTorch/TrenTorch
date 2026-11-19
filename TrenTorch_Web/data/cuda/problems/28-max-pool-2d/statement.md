## Statement

Max pooling over an `H x W` image with window `PH x PW` and strides `SH`, `SW`, **no padding**. The output has $O_H = \left\lfloor \dfrac{H - P_H}{S_H} \right\rfloor + 1$ rows and $O_W = \left\lfloor \dfrac{W - P_W}{S_W} \right\rfloor + 1$ columns (integer division), and `Y[oy][ox]` is the maximum of the window starting at `(oy * SH, ox * SW)`.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void maxpool2d(const float* X, float* Y, int H, int W, int OH, int OW, int PH, int PW, int SH, int SW)</p>

### How it is launched

2D blocks of `(16, 16)` covering the **output** (`x` over `OW`, `y` over `OH`).

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- All values are negative in some tests, so start the running maximum at `-INFINITY`, not at 0.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
