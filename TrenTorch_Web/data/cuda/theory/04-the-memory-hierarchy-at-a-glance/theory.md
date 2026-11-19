# The memory hierarchy at a glance

## A ladder, not a single memory

A GPU has several kinds of memory. Small ones are fast and private; large ones are slow and shared. Almost all CUDA performance work is *moving data to a faster rung and reusing it there*.

| Memory | Scope (who can see it) | Where it lives | Latency *(approx.)* | Size *(approx.)* |
|---|---|---|---|---|
| Registers | one thread | SM register file | ~1 cycle | up to 255 per thread, 64K per SM |
| Shared memory | one block | on the SM | ~20-30 cycles | 48-164 KB per SM (configurable) |
| L1 cache | one SM | on the SM | ~30 cycles | shares space with shared memory |
| L2 cache | all SMs | chip-wide | ~200 cycles | 4-50 MB |
| Global memory | whole grid, and the host | VRAM (GDDR/HBM) | ~400-800 cycles | 16-80 GB |
| Local memory | one thread | *physically in global memory* | like global | spilled registers, big arrays |
| Constant memory | whole grid, read-only | VRAM + dedicated cache | fast if all lanes read the same address | 64 KB |

Latency and size are approximate and differ by chip; the viz reads them from the profile.

## Scope is a contract

A variable in a register belongs to one thread; threads cannot read each other's registers (except with warp shuffles, F1). Shared memory is declared with `__shared__` and is visible to every thread in the same block, and *only* that block. Global memory is the only place blocks can exchange data during a kernel, and only through atomics or by ending the kernel.

## Why this matters

A global load costs hundreds of cycles; a floating-point add costs a handful. If every operand comes from global memory, the arithmetic units wait most of the time. The programmer's job is to use each byte loaded from global memory **as many times as possible** before it is evicted from the fast rungs. Chapters D1-D6 teach how.

## Interactive: The memory pyramid

<div class="cuda-viz" data-viz="VIZ-MEMORY-LADDER" data-title="The memory pyramid" data-spec="VIZ-MEMORY-LADDER"></div>

## Interactive: Who can see what?

<div class="cuda-viz" data-viz="VIZ-SCOPE-VISIBILITY" data-title="Who can see what?" data-spec="VIZ-SCOPE-VISIBILITY"></div>

## Bandwidth and latency tables for sizing

Latency numbers matter for Little's law; capacity matters for blocking.

| Level *(approx., A100)* | Latency (cycles) | Bandwidth per SM / chip |
|---|---|---|
| Register | ~1 | ≈ unbounded for the FMA pipes |
| Shared memory | ~25 | 128 B/cycle/SM → ~19 TB/s chip-wide at 1.41 GHz |
| L1 | ~30 | similar to shared |
| L2 | ~200 | several TB/s chip-wide |
| DRAM (HBM2e) | ~450 | ~2 TB/s chip-wide |

Chip-wide shared bandwidth: 128 B × 1.41 GHz × 108 SMs ≈ **19.5 TB/s**: about **10× DRAM**. That ratio is the headroom that tiling exploits.

## Measuring achievable bandwidth (the copy-kernel benchmark)

$$\text{BW}_{\text{eff}} = \frac{\text{bytes read} + \text{bytes written}}{\text{time}}$$
Example: a copy kernel moves 1 GiB in and 1 GiB out in 1.30 ms: 2 × 1.0737 × 10⁹ ÷ 1.30 × 10⁻³ = 1.65 TB/s = **81%** of the A100's 2,039 GB/s. That number, not the datasheet, is the ceiling every memory-bound kernel in the course is compared against.

## Unified memory and page faults (context only)

`cudaMallocManaged` gives one pointer valid on host and device; the driver migrates pages on demand. First touch on the "wrong" side triggers a page fault and a migration (microseconds each), so the performance rules of A2 (PCIe) still apply, hidden. Use `cudaMemPrefetchAsync` or explicit copies in performance-critical code. *(Not in the simulator.)*

## Check yourself

1. Which memory can two different blocks both write to during a kernel?
2. What is "local memory" really?
3. Why do the fastest memories have the smallest size?
4. Why does effective bandwidth sometimes exceed DRAM bandwidth in a microbenchmark?
5. A copy kernel reaches 1.4 TB/s on a GPU rated 2.0 TB/s. Is that suspicious?

<details class="answers">
<summary>Show answers</summary>

1. Global.
2. Spilled registers / per-thread arrays: physically in global memory.
3. Speed needs proximity and few access ports: small SRAM near the ALUs; large capacity needs distance.
4. L2/L1 hits for a small working set.
5. No: 70% of peak is lower than a typical 80-90%; investigate access pattern/occupancy.

</details>

## Practice

[CU-001 Vector Addition](problem:CU-001): count which levels a load and a store touch.

*PMPP reference:* Ch. 5 (memory types, scoping, the compute-to-global-memory-access ratio), Ch. 6 (achievable bandwidth, coalescing).
