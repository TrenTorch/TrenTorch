## Statement

Given two vectors `A` and `B` of `N` floats, write $C_i = A_i + B_i$ for every `i`.

Every output must be written exactly once, and no thread may touch an index $i \ge N$.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void vector_add(const float* A, const float* B, float* C, int N)</p>

### How it is launched

256 threads per block and $\lceil N / 256 \rceil$ blocks, so there are usually a few more threads than elements.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

### Example

`A = [1, 2, 3]`, `B = [10, 20, 30]` gives `C = [11, 22, 33]`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
