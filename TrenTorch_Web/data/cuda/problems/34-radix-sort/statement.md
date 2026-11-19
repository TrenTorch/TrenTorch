## Statement

Implement one pass of a **stable LSD radix sort** on 1 bit. Given $n \le 1024$ keys in `in`, write them to `out` so that all keys whose bit `bit` is `0` come first, then those whose bit is `1`, **keeping the original relative order inside each group**.

Build it from an **exclusive scan** of the "bit is 0" flags: the scan gives each zero-key its destination, and ones go after all zeros (`zeros_total + i - zeros_before_i`). The tests run the pass for bits 0..9 on keys in `[0, 1024)`, swapping buffers each time, which sorts the keys.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void radix_pass(const int* in, int* out, int n, int bit)</p>

### How it is launched

A **single block of 1024 threads** (one key per thread, so $n \le 1024$). Declare static shared arrays of 1024 entries.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Stability is what makes the passes compose: a scan-based scatter preserves it, a racy one does not.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
