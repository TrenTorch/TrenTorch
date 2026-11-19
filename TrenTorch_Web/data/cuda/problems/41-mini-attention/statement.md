## Statement

Compute scaled dot-product attention for one head: $O = \mathrm{softmax}\!\left(\dfrac{Q K^{\top}}{\sqrt{D}}\right) V$, with `Q, K, V` of shape `T x D` (row-major) and output `O` of shape `T x D`. No mask.

Each **block handles one query row**: compute its `T` scores into shared memory, do a stable softmax over them, then form the weighted sum of the rows of `V`. The `T x T` score matrix is never written to global memory.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void attention(const float* Q, const float* Kmat, const float* V, float* O, int T, int D)</p>

### How it is launched

One block of **64 threads per query row** (`grid = T`). $T \le 64$ and $D \le 64$, so one thread can own one key (for the scores) and one output dimension (for the result). Declare `__shared__ float scores[64];` and a `__shared__ float q[64];`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Subtract the row maximum before `exp`: the large-score cases overflow otherwise.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
