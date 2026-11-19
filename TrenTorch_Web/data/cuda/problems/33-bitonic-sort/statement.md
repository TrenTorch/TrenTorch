## Statement

Implement one **compare-exchange step** of the bitonic sorting network. The tests run the host loops `for (k = 2; k <= n; k *= 2) for (j = k / 2; j > 0; j /= 2)` and launch your kernel once per `(k, j)`.

In each step, thread `i` pairs with `l = i ^ j`. Only the lower index of the pair acts: if `(i & k) == 0` the pair must end **ascending** (`data[i] <= data[l]`), otherwise **descending**. Swap when the pair is out of order.

The network is data-independent: the same comparisons happen for every input, so there is no data-dependent divergence between `if` branches on the keys.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void bitonic_step(float* data, int j, int k, int n)</p>

### How it is launched

One thread per element: 256 threads per block, $\lceil n / 256 \rceil$ blocks, launched repeatedly by the test. `n` is a power of two (the hidden case pads 1000 keys to 1024 with a large sentinel).

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
