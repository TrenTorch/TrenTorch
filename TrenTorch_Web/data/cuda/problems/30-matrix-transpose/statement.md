## Statement

Transpose a row-major `H x W` matrix `A` into the row-major `W x H` matrix `B` ($B_{xy} = A_{yx}$).

A naive kernel reads with unit stride but writes with stride `H`, so half of its accesses are uncoalesced. Stage a tile in shared memory so **both** the global read and the global write are coalesced, and pad the tile (`[32][33]`) so reading a column does not hit one shared-memory bank 32 times.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void transpose(const float* A, float* B, int H, int W)</p>

### How it is launched

2D blocks of `(32, 32)` threads and a $\lceil W / 32 \rceil$ by $\lceil H / 32 \rceil$ grid. One block handles one 32x32 tile.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- **Submit also checks efficiency** on a 64x64 case: coalescing efficiency must be at least 85% and the kernel must have no shared-memory bank conflicts. A naive transpose is correct but does not pass that check.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
