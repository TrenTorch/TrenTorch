## Statement

For each row of logits `Z[r][0..K)` and integer class `target[r]`, compute $\text{loss}_r = \log\sum_k e^{Z_{rk}} - Z_{r,\,t_r}$.

Compute the log-sum-exp stably: $m + \log\sum_k e^{z_k - m}$. Some rows hold logits near 1000.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void cross_entropy(const float* Z, const int* target, float* loss, int rows, int K)</p>

### How it is launched

One block of **128 threads per row** (`grid = rows`). Rows can be wider than the block, so each thread loops over columns with a stride of `blockDim.x`. Declare your own static shared arrays (`__shared__ float s[128];`). Thread 0 writes `loss[row]`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
