## Statement

Implement **inverted dropout**. Keep each element with probability `keep_prob`: a kept element becomes `X[i] / keep_prob`, a dropped element becomes `0`.

The mask must come from a per-thread **hash of the index and `seed`** (no shared state), so the same seed always gives the same output.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void dropout_hash(const float* X, float* Y, int N, float keep_prob, unsigned seed)</p>

### How it is launched

256 threads per block, $\lceil N / 256 \rceil$ blocks.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- `keep_prob = 1` must return `X` unchanged and `keep_prob = 0` must return all zeros.
- The tests check the kept fraction on 4000 elements (within 0.3 of `keep_prob`), that the same seed twice gives identical output, and that survivors are scaled by `1 / keep_prob`.
- Integer math in the simulator is done in doubles, so keep your hash products below 2^53 (for example an LCG such as `r = (i ^ seed) * 1103515245 + 12345`, then reduce with `%`).

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
