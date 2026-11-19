## Statement

Compute $C = AB$ with **shared-memory tiling**: each 16x16 block loads one 16x16 tile of `A` and one of `B` into shared memory, synchronizes, accumulates 16 partial products from the tiles, synchronizes again, and moves to the next tile along `K`.

Tiles that hang over the matrix edge must be padded with zeros.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void matmul_tiled(const float* A, const float* B, float* C, int M, int N, int K)</p>

### How it is launched

2D blocks of `(16, 16)`, `TILE = 16`. Grid $\lceil N / 16 \rceil$ by $\lceil M / 16 \rceil$.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- **Submit also checks reuse** on a 32x32x32 case: the kernel must issue fewer than a quarter of the $2MNK$ global loads a naive kernel needs, and must use shared memory.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
