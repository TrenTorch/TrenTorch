## Statement

Two simulated GPUs run an `AllReduce` followed by a `Broadcast`. Rank 0 issues them in one order and rank 1 in the other, so the ranks wait for **different collectives** and a real cluster would hang. The simulator reports the order mismatch instead. Fix the host code so every rank issues the same collectives in the same order.

After the fix both ranks must print the reduced value `3` (the sum of `1` and `2`).

### Kernel signature

Keep the name and parameters exactly as written (and every kernel listed, even ones that look easy). The tests allocate the buffers, launch your kernels, and read the result back.

<p class="cuda-signature">int main()   // the bug is in the per-rank collective calls</p>

### How it is launched

Run with **2 devices**.

### Rules
- The simulator checks every memory access. Reading or writing outside an array fails the test and names the block and thread.
- The rule: every rank executes the same sequence of collectives, with matching counts, types, reduction ops and roots.

**Run** checks the first two visible cases and shows a performance report. **Submit** also runs hidden cases.
