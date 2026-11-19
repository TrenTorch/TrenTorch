## Statement

LayerNorm of each row of a `rows x K` matrix: $Y_{rj} = \dfrac{X_{rj} - \mu}{\sqrt{\sigma^2 + \varepsilon}}\,\gamma_j + \beta_j$, where `mean` and the **population** variance `var = mean((x - mean)^2)` are taken over the row.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void layer_norm(const float* X, const float* gamma, const float* beta, float* Y, int rows, int K, float eps)</p>

### How it is launched

One block of **128 threads per row** (`grid = rows`). Rows can be wider than the block, so each thread loops over columns with a stride of `blockDim.x`. Declare your own static shared arrays (`__shared__ float s[128];`). `eps` is `1e-5`. Test rows have a large offset, so compute the variance from deviations (two-pass or Welford), not from `E[x²] - E[x]²`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
