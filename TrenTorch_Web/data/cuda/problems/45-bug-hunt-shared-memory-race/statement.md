## Statement

This kernel should reverse the order of the 128 elements inside each block: `out[b*128 + t] = in[b*128 + 127 - t]`. It gives wrong results and the simulator flags a **shared-memory race**. Find the bug and fix it.

Start from the code in the editor (the bug is already there). Do not change the kernel signature.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void block_reverse(const float* in, float* out, int n)</p>

### How it is launched

128 threads per block, `n / 128` blocks (`n` is a multiple of 128).

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Read the diagnostic: it names the block and thread involved.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
