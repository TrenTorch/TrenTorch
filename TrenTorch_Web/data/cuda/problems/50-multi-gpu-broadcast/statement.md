## Statement

Four simulated GPUs. Only **rank 0** holds the data (8 floats, all equal to $7.5$); the other ranks hold zeros. Use **`ncclBroadcast`** so that every rank ends with $7.5$ in its receive buffer.

This problem is a host program: the starter builds the communicators and the buffers and prints the result; you write the collective.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">int main()   // fill in the TODO: one ncclBroadcast call per rank</p>

### How it is launched

The program runs on **4 devices**. Select a device with `cudaSetDevice(r)` before touching its buffers, and make the matching call on every rank, in the same order. The root is rank $0$.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- `ncclBroadcast(send, recv, count, ncclFloat, root, comms[r], 0)`: every rank passes the same `root`.
- The tests read the lines `rank r: value`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
