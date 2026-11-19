## Statement

Four simulated GPUs each hold a **shard** of 4 floats, all equal to $r + 1$ on rank $r$. Use **`ncclAllGather`** so that every rank ends with the **full 16-float tensor**: rank 0's shard first, then rank 1's, and so on. The element at index $4k$ must therefore equal $k + 1$.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">int main()   // fill in the TODO: one ncclAllGather call per rank</p>

### How it is launched

The program runs on **4 devices**. The receive buffer on each rank holds $4 \times 4 = 16$ floats; `sendcount` is the shard size, $4$.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- `ncclAllGather(send, recv, sendcount, ncclFloat, comms[r], 0)`: `sendcount` is the size of **one** shard, not of the result.
- The tests read `rank r: v0 v1 v2 v3`, the first element of each of the four shards as seen by rank `r`.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
