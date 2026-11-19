## Statement

Compute $\cos(a, b) = \dfrac{a \cdot b}{\lVert a \rVert\,\lVert b \rVert}$ and store it in `out[0]`.

Do it in **one pass over the data**: each thread accumulates three values (`dot`, `aa`, `bb`) while it walks its share of the array, the block reduces all three, and each block writes a triple. A second kernel combines the triples and divides.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void cos_partials(const float* A, const float* B, float* partial, int N)<br>__global__ void cos_final(const float* partial, float* out, int blocks)</p>

### How it is launched

`cos_partials`: exactly **8 blocks of 256 threads**, `3 * 256 * 4` bytes of dynamic shared memory (three arrays of 256 floats). Block `b` writes `partial[3*b] = dot`, `partial[3*b+1] = aa`, `partial[3*b+2] = bb`. `cos_final`: one block of 32 threads, `3 * 32 * 4` bytes of dynamic shared memory, `blocks = 8`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
