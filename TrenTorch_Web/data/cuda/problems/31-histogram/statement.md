## Statement

Count how often each value in `[0, bins)` occurs in the integer array `x`: $\text{hist}_b = \#\{\, i : x_i = b \,\}$. `hist` is zero before the launch.

Global atomics are correct but every thread fights over the same few counters. Try privatizing: give each block its own histogram in shared memory, then merge it into the global one.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void histogram(const int* x, unsigned* hist, int n, int bins)</p>

### How it is launched

256 threads per block, $\lceil n / 256 \rceil$ blocks. $\text{bins} \le 64$.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Ignore keys outside `[0, bins)`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
