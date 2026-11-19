## Statement

Apply ReLU using **128-bit vector loads and stores** (`float4`). Each thread handles four consecutive elements, and the last `N mod 4` elements (the *tail*) must also be processed in the same launch.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void relu_float4(const float* X, float* Y, int N)</p>

### How it is launched

128 threads per block and $\lceil (\lfloor N/4 \rfloor + 3) / 128 \rceil$ blocks, so there are enough threads to cover the vector part **and** the at most 3 tail elements.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Buffers are 16-byte aligned. A misaligned `float4` access fails with `cudaErrorMisalignedAddress`.
- Submit checks that you really issued `float4` loads (about 16 bytes per load instruction), not four scalar loads.
- Total bytes moved stay `8N`: vectorizing saves instructions, not traffic.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
