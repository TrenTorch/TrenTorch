## Statement

Write a SAXPY kernel $y_i = a\,x_i + y_i$ that is **correct for any launch configuration**: any block size from 32 to 1024 and any number of blocks, including a grid too small to cover the array. A grid-stride loop does this.

Then open the **Console** report of each case: the tests launch the same kernel with block sizes 32, 64, 128, 256, 512 and 1024. Compare the occupancy and the modelled time, and decide which block size you would pick and why (the simulator reports its own occupancy model; on real hardware you would confirm with a profiler).

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void saxpy_any_block(float a, const float* x, float* y, int n)</p>

### How it is launched

Six cases with $\lceil n / \text{block} \rceil$ blocks for `block` in `{32, 64, 128, 256, 512, 1024}`, plus a case with only **3 blocks of 128 threads** for `n = 3000`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- This problem is about reading the report, not about a single right block size: any correct kernel passes.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
