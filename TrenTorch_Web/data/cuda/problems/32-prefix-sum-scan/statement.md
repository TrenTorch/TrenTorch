## Statement

Compute the **inclusive prefix sum** $y_i = \sum_{j=0}^{i} x_j$ of an array of any length, using the standard three-stage multi-block scheme:

1. `scan_blocks`: each block scans its own 256 elements in shared memory and writes its **total** to `sums[blockIdx.x]`.
2. `scan_sums`: one block scans the block totals in place.
3. `add_offsets`: block `b > 0` adds the scanned total of block `b - 1` to every element of its segment.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void scan_blocks(const float* x, float* y, float* sums, int n)<br>__global__ void scan_sums(float* sums, int nb)<br>__global__ void add_offsets(float* y, const float* sums, int n)</p>

### How it is launched

`scan_blocks`: 256 threads per block, $\lceil n / 256 \rceil$ blocks, `256 * 4` bytes of dynamic shared memory. `scan_sums`: one block of 32 threads (`nb <= 32`). `add_offsets`: 256 threads per block, $\lceil n / 256 \rceil$ blocks. Values are small integers, so the result is exact.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Pad past-the-end lanes with `0`, and keep every thread reaching every `__syncthreads()`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
