## Statement

This is the heart of **distributed data-parallel training**. Four GPUs each computed a local gradient (the starter fills rank $r$'s 8-element gradient with the value $r + 1$). Average the gradients across the GPUs so every rank holds the same mean, $\bar g = \frac{1}{P}\sum_r g_r = 2.5$.

You write two things: the kernel `scale_grad`, which multiplies every element by a factor, and the host code that **sums** the gradients with `ncclAllReduce` and then **scales** the sum by $1/P$ with your kernel.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">__global__ void scale_grad(float* g, int n, float factor)<br>int main()   // sum with ncclAllReduce, then launch scale_grad on every rank</p>

### How it is launched

The program runs on **4 devices**. Launch `scale_grad` with 256 threads per block and $\lceil n / 256 \rceil$ blocks on each device, after `cudaSetDevice(r)`.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- Use the receive buffer of the AllReduce as the input of your kernel.
- The tests read `rank r: value` and expect $2.5$ on every rank.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
