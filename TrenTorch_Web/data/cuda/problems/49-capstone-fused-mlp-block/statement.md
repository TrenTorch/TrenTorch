## Statement

Put the ladder together: compute the forward pass of a two-layer MLP block, $Y = \mathrm{ReLU}(XW_1 + b_1)\,W_2 + b_2$, with two kernels.

- `mlp_layer1` computes the hidden activations $H = \mathrm{ReLU}(XW_1 + b_1)$ (a fused matmul + bias + ReLU, as in *Fused MatMul + Bias + ReLU*).
- `mlp_layer2` computes $Y = H W_2 + b_2$ (matmul + bias, no activation).

Shapes: `X[M][Din]`, `W1[Din][Dh]`, `b1[Dh]`, `Hid[M][Dh]`, `W2[Dh][Dout]`, `b2[Dout]`, `Y[M][Dout]`, all row-major. (The source handbook entry for this capstone was cut off, so this definition is the one used here.)

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void mlp_layer1(const float* X, const float* W1, const float* b1, float* Hid, int M, int Din, int Dh)<br>__global__ void mlp_layer2(const float* Hid, const float* W2, const float* b2, float* Y, int M, int Dh, int Dout)</p>

### How it is launched

Both kernels use 2D blocks of `(16, 16)` with `x` over output columns and `y` over rows.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
