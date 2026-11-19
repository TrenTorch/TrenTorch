# Memory ordering, fences and atomics

## Why `__syncthreads()` is not the whole story

`__syncthreads()` orders memory for **one block**. Blocks run independently, and threads can see each other's global writes in different orders unless you say otherwise. CUDA gives you three kinds of tools.

## Fences

- `__threadfence_block()`: writes before the fence are visible to the block before writes after it.
- `__threadfence()`: the same, but visible to *all threads on the device*.
- `__threadfence_system()`: also to host / other GPUs.

A fence orders **this thread's own** memory operations. It does *not* make other threads wait. Waiting needs a barrier, a flag, or an atomic.

## The "last block done" pattern

How do you finish a multi-block reduction in **one** kernel? Each block writes its partial result, issues `__threadfence()`, then does `atomicAdd(&counter, 1)`. The block that gets `counter == gridDim.x − 1` knows every other block's partial is visible and performs the final combine.
```cuda
/* write partial[blockIdx.x]; __threadfence();
   ticket = atomicAdd(&counter, 1);
   if (ticket == gridDim.x - 1) { /* final sum over partial[] */ } */
```
Without the fence, the last block can read a stale `partial[]` entry. The classic bug is forgetting the fence or reading the partials through a non-volatile cached path.

## Atomics: semantics and cost

`atomicAdd`, `atomicMax`, `atomicCAS`, `atomicExch` perform an indivisible read-modify-write. They execute in the L2 for global memory (≈ one result per cycle per address, with many addresses in parallel) and in the SM for shared memory.
- **Same-address contention** serializes: if 90% of N = 2²⁶ updates hit one bin at roughly 1 ns each, that is ≈ 60 ms of serialization *(illustrative)* versus ≈ 0.3 ms for the same traffic spread across bins.
- **`atomicCAS` loops** build any missing atomic (e.g., float `atomicMax`) but can retry under contention.
- **Float atomics are non-deterministic in order**, so sums differ run to run in the last digits (E2).

## Visibility and `volatile`

`volatile` stops the compiler from caching a global/shared value in a register; it is how spin-wait flags are read. Spinning on a flag written by *another block* is dangerous: if that block is not yet resident (no free SM slot) it may never run → deadlock. This is the formal reason behind "blocks cannot wait for each other" (B2).

## Tools to find these bugs

`compute-sanitizer` has four tools: `memcheck` (out-of-bounds), `racecheck` (shared-memory races), `synccheck` (illegal barrier use), `initcheck` (uninitialized reads). The simulator's diagnostics map onto these (F5).

## Interactive: Who finishes last?

<div class="cuda-viz" data-viz="VIZ-LAST-BLOCK" data-title="Who finishes last?" data-spec="VIZ-LAST-BLOCK"></div>

## Check yourself

*PMPP reference:* Ch. 9 (atomic operations, throughput and contention, privatization), Ch. 11 (single-pass scan and inter-block coordination), Ch. 22 (advanced practices).

1. What does `__threadfence()` guarantee, and what does it not?
2. Why can spin-waiting on another block's flag deadlock?
3. How many global atomics does the last-block pattern issue for a grid of 1,000 blocks?

<details class="answers">
<summary>Show answers</summary>

1. orders this thread's own writes for visibility device-wide; does not make others wait.
2. the other block may not be resident.
3. 1,000.

</details>
