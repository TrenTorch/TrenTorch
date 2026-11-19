## Statement

Compute $C = AB$ where **each thread computes a 2x2 block of outputs** instead of one. Loading one fragment of `A` and one of `B` now feeds four accumulators, which cuts index arithmetic and loads per FLOP.

The launch only has a quarter of the threads, so a one-output-per-thread kernel computes only part of `C` and fails.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void matmul_coarsened(const float* A, const float* B, float* C, int M, int N, int K)</p>

### How it is launched

2D blocks of `(8, 8)` threads. Each block covers a **16 x 16** tile of `C`; grid $\lceil N / 16 \rceil$ by $\lceil M / 16 \rceil$. Thread `(tx, ty)` owns rows `by*16 + ty*2 .. +1` and columns `bx*16 + tx*2 .. +1`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
