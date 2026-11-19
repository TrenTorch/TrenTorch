## Statement

Compute the element-wise product $C_i = A_i \cdot B_i$ of two length-`N` vectors.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void hadamard(const float* A, const float* B, float* C, int N)</p>

### How it is launched

256 threads per block, $\lceil N / 256 \rceil$ blocks.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

### Example

`A = [1, 2, 3]`, `B = [4, 5, 6]` gives `C = [4, 10, 18]`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
