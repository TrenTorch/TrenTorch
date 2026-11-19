## Statement

Four simulated GPUs each hold 8 floats with $x_i = (r + 1)(i + 1)$ on rank $r$. Use **`ncclReduceScatter`** to sum them across ranks **and** split the result: rank $k$ receives only its own 2-element shard of the sum, elements $2k$ and $2k+1$.

Since $\sum_r (r+1) = 10$, the summed vector is $10\,(i+1)$, so rank 0 gets $[10, 20]$, rank 1 gets $[30, 40]$, rank 2 gets $[50, 60]$ and rank 3 gets $[70, 80]$.

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">int main()   // fill in the TODO: one ncclReduceScatter call per rank</p>

### How it is launched

The program runs on **4 devices**. `recvcount` is the size of **one rank's shard**, $2$; the send buffer has $4 \times 2 = 8$ elements.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- `ncclReduceScatter(send, recv, recvcount, ncclFloat, ncclSum, comms[r], 0)`.
- The tests read `rank r: a b`, the two elements rank `r` received.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
