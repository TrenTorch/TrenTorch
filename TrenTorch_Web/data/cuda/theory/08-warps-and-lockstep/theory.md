# Warps and lockstep

## The warp is the real unit

The hardware does not schedule single threads. It cuts each block into **warps** of exactly **32 threads** and schedules warps. A warp's 32 lanes execute the same instruction in the same cycle. Everything about speed on a GPU (coalescing, divergence, bank conflicts) is a statement about *what the 32 lanes of one warp do together*.

<div class="cuda-diagram" data-diagram="warps-in-block" data-title="A block cut into warps"></div>

## Linearized thread id → warp and lane

Take the linearized id from B1: `warp = tid / 32`, `lane = tid % 32`. For a 1D block of 256 threads that is 8 warps. For a 2D block the **x index varies fastest**, so:

| Block shape | Threads | Warps | What one warp holds |
|---|---|---|---|
| 256 × 1 | 256 | 8 | 32 consecutive x values of one row |
| 16 × 16 | 256 | 8 | **two** full rows (16 x-values × 2 y-values) |
| 8 × 8 | 64 | 2 | **four** rows of 8 |
| 33 × 1 | 33 | 2 | 32 threads + **one** thread (31 lanes idle) |

Block sizes that are not multiples of 32 waste lanes in the last warp.

## Scheduling and latency hiding

Each SM has four warp schedulers; each cycle each picks a **ready** warp and issues its next instruction. When a warp issues a global load it must wait hundreds of cycles for data. A CPU would stall; a GPU simply **switches to another resident warp**, at zero cost, because every warp's registers stay resident in the SM's register file. This is how the GPU hides memory latency: not with big caches, but by always having other work.

How many warps are "enough"? Use Little's law: data in flight = latency × bandwidth. On an A100, ~2 TB/s × ~400 ns ≈ 800 KB must be in flight across the chip *(approx.)*, about 7 KB per SM, which is roughly 58 warp-wide 128-byte loads outstanding per SM. That is why each SM wants many resident warps.

## Interactive: How a block is sliced into warps

<div class="cuda-viz" data-viz="VIZ-WARP-FORMATION" data-title="How a block is sliced into warps" data-spec="VIZ-WARP-FORMATION"></div>

## Interactive: Never wait

<div class="cuda-viz" data-viz="VIZ-LATENCY-HIDING" data-title="Never wait" data-spec="VIZ-LATENCY-HIDING"></div>

## Issue-slot accounting

An SM has 4 schedulers; each can issue one instruction per cycle. For a kernel whose instruction stream has *m* memory instructions of latency *L* cycles per *c* compute instructions, the number of warps per scheduler needed to hide latency is roughly
$$W_{\text{needed}} \approx 1 + \frac{L}{c \cdot \text{CPI}}$$
where CPI is the cycles one warp's compute instruction occupies the scheduler (2 for FP32 on the A100). Example: L = 450, c = 4 compute instructions between loads: 1 + 450/(4×2) ≈ **57 warps per scheduler**, which exceeds the 16 warps per scheduler the hardware holds (64 per SM ÷ 4). Conclusion: this kernel is latency-bound at *any* occupancy unless you add ILP (more independent loads per thread) or increase *c*. The viz VIZ-LATENCY-HIDING should expose this formula.

## ILP versus TLP

- **TLP** (thread-level parallelism): more warps.
- **ILP**: independent instructions within a warp, e.g., unroll a loop with 4 independent accumulators and issue 4 loads before using any.
Both fill the same issue slots. Prefer ILP when registers allow, since it needs less occupancy and fewer registers *per useful operation* than it appears.

## Partial warps and lane utilization formula

$$\text{lane utilization} = \frac{B}{32 \cdot \lceil B/32 \rceil}$$
B = 100: 100/128 = 78.1% (matches "28 lanes wasted"). B = 33: 33/64 = 51.6%. The viz already shows this; make the formula visible on hover.

## Interactive: ILP or more warps?

<div class="cuda-viz" data-viz="VIZ-ISSUE-SLOTS" data-title="ILP or more warps?" data-spec="VIZ-ISSUE-SLOTS"></div>

## Check yourself

1. A block is 100 threads. How many warps, and how many lanes are wasted?
2. In a 16 × 16 block, which two rows share warp 0?
3. Why is switching between warps free?
4. A kernel has 3 compute instructions between dependent loads, L = 400, CPI = 2. Estimate warps per scheduler needed.
5. What is the lane utilization of a 20 × 20 block?

<details class="answers">
<summary>Show answers</summary>

1. 4 warps; 28 lanes wasted.
2. Rows 0 and 1.
3. all state stays resident in the register file.
4. 1 + 400/(3·2) ≈ 68 warps per scheduler: beyond the hardware, so add ILP.
5. 400/416 = 96.2%.

</details>

## Pitfalls

- Block sizes that are not multiples of 32.
- Using tiny blocks (like 32) that leave too few warps resident per SM.

## Practice

[CU-009 Matrix Addition](problem:CU-009) · [CU-018 Mean and Variance](problem:CU-018)

*PMPP reference:* Ch. 4 (warps, SIMD execution, latency tolerance, warp scheduling), Ch. 6 (occupancy vs ILP discussion in performance considerations).
