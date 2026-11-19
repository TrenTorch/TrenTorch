# Registers, local memory, constant and read-only cache

## Registers

The fastest storage. Each thread can use up to 255 registers, but every register a thread uses is one fewer available to other threads on the SM, so heavy register use lowers occupancy (B4). If a thread needs more than the compiler can allot, values **spill** into **local memory**, which is actually global memory (cached), and the kernel slows down. You can steer the compiler with `__launch_bounds__(maxThreads)` or `-maxrregcount`.

## Local memory

Per-thread arrays with dynamic indexing, and spilled registers, live here. It is private, but it is as slow as global memory (aside from caching), so avoid big per-thread arrays.

## Constant memory

A 64 KB read-only region with a dedicated cache. It is ideal for small data that every thread reads: a convolution filter, a lookup table, kernel parameters. When **all lanes of a warp read the same address**, the value is broadcast in one step. If lanes read *different* constant addresses, the reads serialize, so do not use it for per-thread indexing into a big table.

## The read-only path

Marking inputs `const float* __restrict__` tells the compiler the data is not written through other pointers and aliasing is absent, so it can use the read-only cache path and schedule loads more aggressively.

## Interactive: The register budget

<div class="cuda-viz" data-viz="VIZ-REGISTER-PRESSURE" data-title="The register budget" data-spec="VIZ-REGISTER-PRESSURE"></div>

## Register budget arithmetic

For 100% occupancy on the A100 at 256-thread blocks you need ≤ 32 registers/thread (table in B4). `__launch_bounds__(maxThreadsPerBlock, minBlocksPerSM)` asks the compiler to fit: `__launch_bounds__(256, 8)` ⇒ ≤ 65,536 ÷ (256×8) = **32 registers**. If the kernel genuinely needs 48, the compiler spills 16 values per thread to local memory. Each spill is a store and a later load: the extra DRAM/L1 traffic is `spilled values × threads × 4 B × 2`. For 1M threads and 16 spills that is 128 MB of unnecessary traffic.

## Reading `-Xptxas -v` output

Report fields to check: registers per thread, spill stores/loads (bytes), shared memory per block, constant memory. The simulator should print the same fields in the run report (F5).

## Constant memory broadcast arithmetic

Constant cache serves **one address per cycle** per SM *(approx.)*. If all 32 lanes read the same address: 1 cycle. If lanes read *d* distinct addresses: *d* cycles. A 5×5 filter (25 weights, same for all threads, read in the same order) is 25 broadcast reads ≈ 25 cycles per output, with no global traffic. Putting the same filter in global memory costs 25 cached loads per thread.

## Check yourself

1. Where does a spilled register live?
2. Which memory suits a 5×5 convolution filter read by every thread?
3. Why might `__restrict__` change performance?
4. A100: block 256, `__launch_bounds__(256, 6)`. Register cap per thread?
5. Constant-memory read where lane *i* reads `c[i]` (32 different addresses): cycles?

<details class="answers">
<summary>Show answers</summary>

1. local (global-backed).
2. constant.
3. enables the read-only path / better scheduling.
4. 65,536/(256×6) = 42 registers.
5. 32 cycles (serialized distinct addresses).

</details>

## Practice

[CU-026 1D Convolution](problem:CU-026) · [CU-027 2D Convolution](problem:CU-027)

*PMPP reference:* Ch. 5 (constant memory, registers, local memory), Ch. 7 (constant memory for filters, tiled convolution).
