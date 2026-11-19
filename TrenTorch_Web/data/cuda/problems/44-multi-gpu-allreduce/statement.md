## Statement

Four simulated GPUs each hold 8 floats, all equal to `(rank + 1) * 1.5`. Write the host code that sums them across the GPUs with **`ncclAllReduce`** so that **every GPU** ends with the sum in its receive buffer (`1.5 + 3 + 4.5 + 6 = 15`).

This problem is a whole host program, not a kernel: the starter creates the communicators, buffers and the verification printout; you write the collective.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">int main()   // fill in the TODO: one ncclAllReduce call per rank</p>

### How it is launched

The program is run by the simulator with **4 devices**. Select each device with `cudaSetDevice(r)` before using its buffers, and issue the collective on every rank, in the same order.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- `ncclAllReduce(send, recv, count, ncclFloat, ncclSum, comms[r], 0)`: every rank must make the matching call or the collective never completes.
- The tests read the lines printed by `printf("rank %d: %f\n", ...)`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
