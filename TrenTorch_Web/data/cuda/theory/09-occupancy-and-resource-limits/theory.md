# Occupancy and resource limits

## What occupancy is

**Occupancy** = (resident warps on an SM) ÷ (maximum warps the SM supports). It measures how much latency-hiding capacity you have. More resident warps usually means better latency hiding, up to a point.

## Four limits; the smallest wins

Per SM *(approx., differs by architecture)*:

| Limit | T4 (Turing) | A100 (Ampere) |
|---|---|---|
| Max threads per SM | 1,024 | 2,048 |
| Max blocks per SM | 16 | 32 |
| Registers per SM | 65,536 | 65,536 |
| Shared memory per SM | up to 64 KB | up to 164 KB |

For your kernel, compute how many blocks fit under each limit; the minimum is the answer.

**Worked example.** Block = 256 threads, kernel uses 64 registers/thread, no shared memory.
- Registers per block = 256 × 64 = 16,384 → 65,536 / 16,384 = **4 blocks**.
- Thread limit: A100 2,048 / 256 = 8; T4 1,024 / 256 = 4.
- So A100: 4 blocks = 1,024 threads = 50% occupancy (**registers** are the limiter). T4: 4 blocks = 1,024 threads = 100% occupancy.

Same kernel, different occupancy on different chips.

## More is not always better

High occupancy hides latency, but a kernel that uses more registers per thread (to keep values close) can run faster at lower occupancy. Use occupancy as a diagnostic: if a memory-bound kernel runs at 12%, raise it; if it is already high, look elsewhere.

## Choosing a block size

Multiples of 32; 128 or 256 is a common starting point; check the occupancy limiter; try a few sizes and measure.

## Interactive: What limits me?

<div class="cuda-viz" data-viz="VIZ-OCCUPANCY-CALC" data-title="What limits me?" data-spec="VIZ-OCCUPANCY-CALC"></div>

## Allocation granularity (why 37 registers is really 40)

Hardware allocates registers **per warp in fixed-size units** (commonly 256 registers per warp on recent architectures *(approx.)*), which means registers per thread are effectively rounded **up to a multiple of 8**; shared memory is allocated in granules (e.g., 1 KB) as well.

Worked example, A100: block = 128 threads, **37** registers/thread.
- Effective regs/thread = 40; per block 40 × 128 = 5,120.
- 65,536 ÷ 5,120 = 12.8 → **12 blocks** = 1,536 threads = **75%** occupancy.
- Ignoring granularity you would predict 65,536 ÷ 4,736 = 13.8 → 13 blocks (81%): off by one block.
Use `cudaOccupancyMaxActiveBlocksPerMultiprocessor` as ground truth; the calculator viz must apply the rounding rule and say so.

## Register limit → max occupancy table (A100, 2,048 threads/SM, block 256)

| Regs/thread | Regs/block | Blocks (regs) | Threads/SM | Occupancy |
|---|---|---|---|---|
| 32 | 8,192 | 8 | 2,048 | 100% |
| 40 | 10,240 | 6 | 1,536 | 75% |
| 64 | 16,384 | 4 | 1,024 | 50% |
| 80 | 20,480 | 3 | 768 | 37.5% |
| 128 | 32,768 | 2 | 512 | 25% |
| 255 (→256) | 65,536 | 1 | 256 | 12.5% |

For 100% occupancy at 256-thread blocks the compiler must keep **≤ 32 registers/thread**. `__launch_bounds__(256, 8)` asks it to try.

## When low occupancy wins

At 25% occupancy a thread with 128 registers can hold a register-resident 8×8 output tile (64 accumulators). Bandwidth demand from shared memory falls (D4), arithmetic intensity rises, and well-tuned GEMM kernels run at **8-25% occupancy** yet near peak FLOPs. Occupancy is a *tool to hide latency*, not a goal. If you are not latency-bound, extra warps give nothing.

## Wave quantization with resident-block capacity

Given capacity C = SMs × blocksPerSM, a grid of G blocks:
$$\text{efficiency} = \frac{G}{C \cdot \lceil G / C \rceil}$$
G = 2,000, C = 864 → waves = 3, efficiency = 2,000 ÷ 2,592 = **77%**. If the blocks run for similar durations you lose 23% of throughput. Mitigations: grid-stride loops with G = C; change block size to change C; or split the work into more, smaller blocks so the tail wave is short.

## Interactive: Occupancy Staircase

<div class="cuda-viz" data-viz="VIZ-OCCUPANCY-CALC" data-mode="occupancy-staircase" data-title="Occupancy Staircase" data-spec="VIZ-OCCUPANCY-STAIRCASE"></div>

## Check yourself

1. 128 threads/block, 32 regs/thread, 16 KB shared per block, A100 profile. Which limit binds?
2. Why can lowering registers per thread raise occupancy?
3. Name a case where lower occupancy can be faster.
4. A100, block 512 threads, 40 regs/thread, no shared memory: which limit binds and what is the occupancy?
5. G = 1,000 blocks, C = 864. Wave efficiency?
6. Why can a GEMM at 25% occupancy beat one at 100%?

<details class="answers">
<summary>Show answers</summary>

1. Shared memory binds: 164/16 = 10 blocks = 1,280 threads = 62.5%.
2. more blocks fit.
3. high-ILP/register-tiled compute-bound kernels.
4. 40 × 512 = 20,480 regs/block ⇒ 65,536 ÷ 20,480 = 3 blocks = 1,536 threads = **75%**; limiter: registers.
5. 1,000/(2·864) = 57.9%.
6. the register tile lifts AI and cuts shared traffic.

</details>

## Practice

[CU-040 Block-Size Sweep](problem:CU-040)

*PMPP reference:* Ch. 4 (resource partitioning, occupancy calculation, queries), Ch. 6 (performance considerations: register pressure and its trade-offs).

## Further reading

- Volkov, "Better Performance at Lower Occupancy" (GTC 2010)
