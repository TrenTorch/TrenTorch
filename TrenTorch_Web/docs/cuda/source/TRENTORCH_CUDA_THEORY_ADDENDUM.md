# TrenTorch CUDA: Theory Addendum (depth, calculations, advanced topics)

> Companion to `TRENTORCH_CUDA_THEORY.md`. Same rules apply: chapter IDs, `##` anchors = section slugs, all prose original, partial code only (`/* ... */`), *(approx.)* numbers come from the GPU-profile JSON, *(spec)* numbers are published specs.

## How the agent should merge this file

1. **`# APPEND TO <ID>` blocks**: append the block's `##` sections to the *end of the existing chapter's body*, **before** its "Check yourself". Do not rename or delete existing headings.
2. **`# NEW CHAPTER <ID>` blocks**: create new MDX files exactly like existing chapters. New IDs: `A5, C3, E9, E10, F7, F8, F9, G1`. Also apply the `# VISUALIZATION GAP-FILL` block: each spec there belongs at the end of the chapter named in its heading. Add them to `meta.json` in the order given in the "Reading order" table.
3. **`🎬` blocks** are additional viz specs following the same visual language and shared primitives (`LaneStrip`, `MemoryGrid`, `Stepper`, `ReadoutBar`, `TermChip`). Build the pure-TypeScript model first. Every formula in this file must exist as a tested function in `lib/cuda/model/` so the viz and the problem reports use the *same* numbers.
4. **Answer key** (last section) is rendered behind a `<details>` "Show answers" toggle, never inline.
5. **Proposed new problems** (`CU-053+`) are *proposals*; they need plan updates before IDs are final.
6. Numbers labelled "illustrative" are teaching numbers, not benchmarks. Never present them as measured results.

## A note on the PMPP references

All references are to **Programming Massively Parallel Processors, 4th edition (Hwu, Kirk, El Hajj)**, by chapter number and topic. Chapter map used throughout:

| PMPP ch. | Topic | PMPP ch. | Topic |
|---|---|---|---|
| 1 | Introduction | 13 | Sorting |
| 2 | Heterogeneous data-parallel computing | 14 | Sparse matrix computation |
| 3 | Multidimensional grids and data | 15 | Graph traversal |
| 4 | Compute architecture and scheduling | 16 | Deep learning |
| 5 | Memory architecture and data locality | 17 | Iterative MRI reconstruction |
| 6 | Performance considerations | 18 | Electrostatic potential map |
| 7 | Convolution | 19 | Parallel programming and computational thinking |
| 8 | Stencil | 20 | Programming a heterogeneous computing cluster |
| 9 | Parallel histogram | 21 | CUDA dynamic parallelism |
| 10 | Reduction | 22 | Advanced practices and future evolution |
| 11 | Prefix sum (scan) | 23 | Conclusion |
| 12 | Merge | | |

**Agent instruction:** cite chapter numbers only (as below) unless the course author has the book open and confirms section numbers. Do not invent section numbers. Topics not in PMPP (FlashAttention, NCCL ring internals, FP8/BF16 details) are marked **"not in PMPP"** and should link to the original papers or vendor docs in the "Further reading" footer instead.

## Reading order (updated)

`A1 → A2 → A3 → A4 → **A5** → B1 → B2 → B3 → B4 → B5 → C1 → C2 → **C3** → D1 → D2 → D3 → D4 → D5 → D6 → E1 → E2 → E3 → E4 → E5 → E6 → E7 → E8 → **E9 → E10** → F1 → F2 → F3 → F4 → F5 → **F7 → F8 → F9** → F6 (capstone) → **G1** (calculation workbook; also usable as a quiz bank from Part A onward)`

---

# NEW CHAPTER A5: The performance calculator
`id: A5 · part: A · est: 40 min · prereqs: A3, A4 · problems: calculation quizzes (G1) · pmpp: Ch. 4, 5, 6`

Every later chapter ends with a number. This chapter gives you the **eleven formulas** that produce those numbers, so you can predict a kernel's runtime *before* you write it, and know when a measurement is suspicious.

## Peak compute from the spec sheet
$$\text{Peak FP32 FLOP/s} = \text{SMs} \times \text{FP32 cores per SM} \times 2 \times f_{\text{clock}}$$
The factor 2 is because a fused multiply-add (FMA) counts as two floating-point operations.

- **T4:** 40 × 64 × 2 × 1.59 GHz ≈ **8.14 TFLOPS** *(boost clock)*.
- **A100:** 108 × 64 × 2 × 1.41 GHz ≈ **19.5 TFLOPS**.
- **H100 SXM:** 132 × 128 × 2 × ~1.98 GHz ≈ **67 TFLOPS**.

The vendor number assumes every core issues an FMA every cycle. Real kernels reach 70-90% on a good day.

## Peak bandwidth from the memory spec
$$\text{BW} = \frac{\text{bus width (bits)}}{8} \times \text{data rate per pin (Gbit/s)}$$
- **T4:** 256 bits ÷ 8 × 10 Gbit/s = **320 GB/s**.
- **A100 80 GB:** 5,120 bits ÷ 8 × ~3.19 Gbit/s ≈ **2,039 GB/s**.

**Achievable** bandwidth for a clean streaming kernel (a plain copy) is typically **80-90%** of this, written η ≈ 0.8-0.9. Always use η × peak for time predictions. Measure η yourself with a copy kernel (chapter D1).

## The ridge point and the roofline
$$\text{Ridge} = \frac{\text{Peak FLOP/s}}{\text{BW}} \quad [\text{FLOP/byte}]$$
$$\text{Attainable FLOP/s} = \min\big(\text{Peak},\; \text{AI} \times \text{BW}\big)$$

## The one-line time model
$$t \;\approx\; \max\!\left(\frac{\text{bytes}}{\eta_m \cdot \text{BW}},\; \frac{\text{FLOPs}}{\eta_c \cdot \text{Peak}}\right) + t_{\text{launch}}$$
`t_launch` is about **3-10 µs** per kernel launch on the host side *(approx.)*. For kernels that run for tens of microseconds it is not negligible (chapter F7).

## Worked example 1: ReLU on 2²⁸ floats (A100)
- N = 268,435,456. Bytes = 8N = 2.147 GB (read + write).
- Memory time at peak: 2.147 GB ÷ 2,039 GB/s = **1.05 ms**. At η = 0.85: **1.24 ms**.
- Compute time: N FLOPs ÷ 19.5 TFLOPS = **13.8 µs**.
- Ratio memory ÷ compute ≈ **75×**. The ALUs are idle > 98% of the time. No amount of arithmetic tuning matters.

## Worked example 2: why a single vector add should not go to the GPU
Setup: `c = a + b`, N elements, data starts on the host. CPU memory bandwidth 50 GB/s; PCIe 4.0 at 25 GB/s each way; A100 on-device 2,039 GB/s.
- CPU time: 12N bytes ÷ 50 GB/s = 2.4 × 10⁻¹⁰ · N s.
- GPU time = copy in (8N B) + copy out (4N B) over PCIe + kernel: 12N ÷ 25 GB/s + 12N ÷ 2,039 GB/s = (4.8 + 0.06) × 10⁻¹⁰ · N s.
- The GPU is about **2× slower for every N**, because the PCIe copy alone costs more than the CPU's entire computation.

Now run *k* kernels on data that stays resident: GPU = 4.8 × 10⁻¹⁰ N + k · 0.059 × 10⁻¹⁰ N vs CPU = k · 2.4 × 10⁻¹⁰ N. The GPU wins when k ≥ 2.05, so **at least 3 chained passes** over the same data. This is the quantitative reason for "keep data on the device" (chapter A2) and for kernel fusion (F3).

## Amdahl's law (and why "10,000 cores" is not "10,000×")
If a fraction *p* of the work is parallel and speeds up by *s*:
$$\text{Speedup} = \frac{1}{(1-p) + p/s}$$
p = 0.9 and s = 100 gives 1 ÷ (0.1 + 0.009) = **9.2×**; even with s → ∞ the ceiling is **10×**. The serial 10% (often the PCIe copy or a host loop) decides the result. **Gustafson's view:** if you can grow the problem with the machine, the serial fraction shrinks, which is why GPUs shine at large problems.

## Little's law for memory
$$\text{bytes in flight} = \text{latency} \times \text{bandwidth}$$
A T4 with 400 ns latency and 320 GB/s needs 128 KB in flight chip-wide: 3.2 KB per SM, or **25 128-byte warp loads outstanding per SM**. If your kernel has too few resident warps, or too few independent loads per warp, you cannot reach peak bandwidth (this is the reason for occupancy, B4, and vector loads, D3).

## Occupancy and wave arithmetic (preview)
$$\text{blocks per SM} = \min\!\Big(\Big\lfloor\tfrac{\text{threads}_{SM}}{B}\Big\rfloor,\ \Big\lfloor\tfrac{\text{regs}_{SM}}{B\cdot r}\Big\rfloor,\ \Big\lfloor\tfrac{\text{smem}_{SM}}{s}\Big\rfloor,\ \text{blocks}_{max}\Big)$$
$$\text{waves} = \Big\lceil \tfrac{\text{grid}}{\text{SMs} \times \text{blocks per SM}} \Big\rceil,\qquad \text{wave efficiency} = \frac{\text{grid}}{\text{waves} \times \text{SMs} \times \text{blocks per SM}}$$

## Transfer time with latency
$$t_{\text{copy}} = \alpha + \frac{D}{B_{\text{PCIe}}}, \qquad \alpha \approx 10\,\mu s$$
For small copies α dominates, so batch small transfers into one.

## 🎬 VIZ-PERF-CALCULATOR: "Predict before you run"
- *Canvas:* left, a form of inputs; right, a live "receipt" showing each term of the time model as a coloured bar (memory term blue, compute term orange, launch term grey) with the winner outlined.
- *Controls:* **Profile**, **Bytes per element**, **FLOPs per element**, **N** (log slider), **η_m** and **η_c** sliders (defaults 0.85 / 0.8), **Data starts on host** checkbox (adds PCIe terms), **Kernels run (k)**.
- *Animation:* sliding **k** from 1 to 8 with *data starts on host* ticked shows the GPU/CPU crossover marker sliding to the left of k = 3.
- *Readouts:* t_mem, t_compute, t_launch, bound, AI, % of roofline, and "CPU vs GPU" winner.
- *Aha moment:* worked example 2 reproduced live; ReLU shows memory ≈ 75× compute.
- *Accessibility:* sentence readout "Memory term 1.24 ms, compute term 0.014 ms, launch 0.005 ms. Memory-bound."

## Check yourself
1. Compute the T4's peak bandwidth if the bus is 256 bits and the data rate is 14 Gbit/s.
2. For AI = 2 FLOP/B on the A100, what is attainable GFLOP/s?
3. Why is "ratio of memory time to compute time" a better diagnosis than "ratio of FLOPs to bytes" alone?

## Pitfalls
- Using peak instead of η × peak for predictions.
- Forgetting the PCIe terms when the data starts on the host.
- Counting an FMA as one FLOP when comparing with vendor TFLOPS.

---

# APPEND TO A1: Why GPUs exist

## Latency versus throughput as numbers
CPU vs GPU is not "fast vs slow", it is a different point on a **latency-throughput trade-off**. Little's law again: *work in flight = throughput × latency*. A CPU core keeps few operations in flight with very low latency; a GPU keeps tens of thousands in flight and tolerates 400+ cycle latency per operation.

| Quantity *(approx., server class)* | CPU | GPU (A100) |
|---|---|---|
| Hardware threads | ~100 | 108 SMs × 2,048 = 221,184 resident |
| Peak FP32 | ~2-4 TFLOPS (AVX-512) | 19.5 TFLOPS |
| DRAM bandwidth | ~50-100 GB/s | ~2,039 GB/s |
| **FLOP per byte (machine balance)** | ~30-60 | **9.6** |
| Cache per thread | MBs | ~tens of bytes |

A GPU's *machine balance* is lower than you would guess, which is why even moderately arithmetic kernels (AI in the tens) become compute-bound on it, and why memory-bound kernels (AI < 1) are the norm in deep learning outside big matmuls.

## Work, span, and why dependency chains hurt
Model a computation as a graph. **Work** *W* = total operations; **span** *S* = longest chain of dependent operations. Ideal parallel time on *p* processors satisfies
$$T_p \ge \max\!\Big(\frac{W}{p},\; S\Big)$$
- Adding two arrays of N numbers: W = N, S = 1. Parallelism = W/S = N.
- Summing N numbers: W = N − 1, S = log₂N (with a tree). Parallelism ≈ N / log₂N.
- Fibonacci recurrence: W = N, S = N. Parallelism ≈ 1, so a GPU cannot help.

This W/S view is how you judge a problem before touching code, and it returns in chapters E2 (reduction), E6 (scan: work-efficient vs depth-efficient) and E8 (sorting).

## Check yourself (additional)
4. A computation has W = 10⁹ and S = 10⁴. What is the maximum useful number of processors?
5. Why does the machine balance of a GPU make arithmetic intensity so important?

*PMPP reference:* Ch. 1 (motivation, CPU vs GPU design goals), Ch. 19 (computational thinking: choosing parallelizable formulations).

---

# APPEND TO A3: Inside the chip

## Instruction throughput per SM, from the specs
A100 SM: four sub-partitions, each with **16 FP32 lanes** *(spec)*. A warp has 32 threads, so one FP32 warp instruction occupies a sub-partition for **2 cycles**. Per SM that is 4 warps issued per 2 cycles = 2 warp-FMAs per cycle = 64 FMA/cycle/SM, which matches "64 FP32 cores per SM".

Consequences you can calculate:
- A100 SM peak = 64 FMA × 2 FLOP × 1.41 GHz = **180 GFLOP/s per SM**; × 108 SMs = 19.5 TFLOPS ✓.
- To keep the FP32 pipes full each sub-partition must issue an FP32 instruction every 2 cycles. If a warp has no ready instruction (waiting on memory or on its own dependency), the slot is wasted unless another warp is ready.
- **Instruction-level parallelism (ILP)** gives *independent instructions inside one thread* (e.g., four independent accumulators). It fills the pipeline with fewer warps, which is why a kernel at 25% occupancy with ILP 4 can match one at 100% occupancy with ILP 1 (see B4).

## Other throughput facts *(approx., A100)*
| Unit | Per SM per cycle |
|---|---|
| FP32 FMA | 64 |
| INT32 | 64 |
| FP64 | 32 |
| SFU (`__expf`, `rsqrtf` approx.) | 16 |
| Load/store (shared memory) | 32 lanes × 4 B = 128 B |

The shared-memory line, **128 B/cycle/SM**, is the figure we use in chapter D4 to show that naive tiling is *shared-memory-bound*.

## The L2 and DRAM view
DRAM is accessed in bursts; the GPU's memory transaction granularity is the **32-byte sector** (D1). L2 sits between the SMs and DRAM; a hit in L2 avoids DRAM traffic entirely and is why measured "effective" bandwidth can exceed DRAM bandwidth for small working sets. Use **DRAM bytes** (not L2 bytes) when you compute AI for a roofline.

## Check yourself (additional)
4. How many cycles does one FP32 warp instruction occupy a 16-lane sub-partition?
5. Why can ILP substitute for occupancy?

*PMPP reference:* Ch. 4 (architecture, scheduling, warp issue, latency tolerance), Ch. 6 (memory transaction granularity and coalescing).

---

# APPEND TO A4: The memory hierarchy at a glance

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

## Check yourself (additional)
4. Why does effective bandwidth sometimes exceed DRAM bandwidth in a microbenchmark?
5. A copy kernel reaches 1.4 TB/s on a GPU rated 2.0 TB/s. Is that suspicious?

*PMPP reference:* Ch. 5 (memory types, scoping, the compute-to-global-memory-access ratio), Ch. 6 (achievable bandwidth, coalescing).

---

# APPEND TO B1: Threads, blocks, grids and indexing

## Generalizing to 3D
Linearized thread id inside a block and the global 3D → 1D index for a volume of `X × Y × Z` stored x-fastest:
$$\text{tid} = t_x + t_y B_x + t_z B_x B_y,\qquad \text{voxel} = (z \cdot Y + y)\cdot X + x$$
with each coordinate computed as `blockIdx.c * blockDim.c + threadIdx.c`. The same "x is the contiguous axis" rule applies (D1).

## Grid size limits and the 2D grid trick
`gridDim.x` ≤ 2³¹ − 1; `gridDim.y`, `gridDim.z` ≤ 65,535. For a huge 1D problem, either use a grid-stride loop (E1) or fold the block index: `blk = blockIdx.x + blockIdx.y * gridDim.x`.

## Integer overflow: when `int` is not enough
`blockIdx.x * blockDim.x` is computed in 32-bit `unsigned`/`int` arithmetic. With N = 3 × 10⁹ floats (12 GB, fits on an 80 GB card) the product wraps around and every thread past 2³¹ reads the wrong element.
```cuda
size_t i = (size_t)blockIdx.x * blockDim.x + threadIdx.x;   // widen BEFORE multiplying
```
Also compute byte offsets in `size_t`. This is a classic "works until the dataset grows" bug.

## Choosing the 2D block shape by warp analysis
For a W-wide row-major matrix and a block `(Bx, By)`: a warp covers `32/Bx` rows when Bx < 32. Each row-segment is `Bx × 4` bytes contiguous. Efficiency of a *row-major* read:
- Bx = 32: one 128 B segment per warp → 4 sectors, 100%.
- Bx = 16: two 64 B segments → 4 sectors, still 100% if each segment is sector-aligned.
- Bx = 8: four 32 B segments → 4 sectors, 100% *if* aligned; but small segments make misalignment cost more (a 32 B segment straddling a sector boundary touches 2 sectors).
Rule: prefer **Bx ≥ 32** (or a multiple of 8 floats) for coalescing; tile heights fill the rest of the block.

## Check yourself (additional)
4. N = 3 × 10⁹. Which variable types must be 64-bit in the index calculation?
5. A 33×33 volume of cells is processed with 8×8×4 blocks. How many blocks in each dimension?

*PMPP reference:* Ch. 2 (index calculation, grid sizing), Ch. 3 (multidimensional grids, linearizing 2D/3D arrays, image blur and matrix examples).

---

# APPEND TO B3: Warps and lockstep

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

## Check yourself (additional)
4. A kernel has 3 compute instructions between dependent loads, L = 400, CPI = 2. Estimate warps per scheduler needed.
5. What is the lane utilization of a 20 × 20 block?

*PMPP reference:* Ch. 4 (warps, SIMD execution, latency tolerance, warp scheduling), Ch. 6 (occupancy vs ILP discussion in performance considerations).

---

# APPEND TO B4: Occupancy and resource limits

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

## 🎬 VIZ-OCCUPANCY-STAIRCASE (extension of VIZ-OCCUPANCY-CALC)
- *Canvas:* x: registers/thread (16 → 255); y: occupancy %. A staircase curve for the chosen block size; marker for the user's current setting; second curve for the other GPU profile.
- *Controls:* **Block size**, **Shared memory/block**, **Show granularity rounding** toggle.
- *Aha moment:* between two stair edges, adding registers is *free*; one register past an edge costs a whole block.

## Check yourself (additional)
4. A100, block 512 threads, 40 regs/thread, no shared memory: which limit binds and what is the occupancy?
5. G = 1,000 blocks, C = 864. Wave efficiency?
6. Why can a GEMM at 25% occupancy beat one at 100%?

*PMPP reference:* Ch. 4 (resource partitioning, occupancy calculation, queries), Ch. 6 (performance considerations: register pressure and its trade-offs).

---

# APPEND TO C1: Warp divergence

## A probability model of divergence
Suppose each lane independently takes the "rare" path A with probability *p*. The warp executes path A if **any** lane takes it, so
$$P(\text{warp executes both}) = 1 - (1-p)^{32} - p^{32}$$
| p | P(diverge) |
|---|---|
| 0.5 | ≈ 1 − 2⁻³¹ ≈ 100% |
| 0.1 | 96.6% |
| 0.02 | 47.6% |
| 0.01 | 27.5% |
| 0.001 | 3.1% |
Even a 1-in-100 rare branch splits more than a quarter of warps. Time per warp = Σ over executed paths. Expected time if path A costs *a*, path B costs *b*:
$$E[t] = b + a \cdot \big(1-(1-p)^{32}\big) \quad\text{(taking B as the common path)}$$
(Neglect the tiny probability that all lanes take A.) If *a* is large (an expensive error-handling branch), keep *p* tiny or move the rare work out of the hot kernel (e.g., collect rare cases and process them in a second kernel).

## Loop divergence: the max-of-32 effect
Each lane loops `n_lane` times with trip counts uniform on {0..7}. The warp loops until the *last* lane finishes: E[max of 32 draws] ≈ **7 − 0.1** ≈ 6.99, while the mean is 3.5. Utilization ≈ 3.5 ÷ 6.99 = **50%**. If trip counts vary widely across lanes (graph degrees, sparse rows), sort or bucket the work so each warp gets similar trip counts (E9).

## Making warps uniform instead of making branches cheaper
- **Sort/bucket by branch key** so neighbouring lanes agree (cost: an extra pass; worthwhile if the branchy work is expensive).
- **Warp-uniform branches**: branch on `warp_id`, not `lane_id`.
- **Split the kernel** by case, launch each on its subset.
- **Predication/select** for short bodies (≲ 4-10 instructions).

## Check yourself (additional)
4. Probability that a warp diverges when each lane takes a branch with p = 0.02?
5. Trip counts are 0..7 uniformly; the loop body is 20 cycles. What is the warp's loop time versus the *average* lane's useful time?

*PMPP reference:* Ch. 4 (control divergence, its performance impact, loop divergence with variable trip counts), Ch. 6 (strategies for reducing divergence, data rearrangement).

---

# NEW CHAPTER C3: Memory ordering, fences and atomics
`id: C3 · part: C · est: 30 min · prereqs: C2, D4 · problems: theory + playground · pmpp: Ch. 9, 11, 22`

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

## 🎬 VIZ-LAST-BLOCK: "Who finishes last?"
- *Canvas:* 6 blocks as columns; each draws "write partial", optional "fence", "ticket". A global counter and a `partial[]` array below.
- *Controls:* **Include `__threadfence()`** toggle; `Stepper`; **Reorder visibility** toggle (forces block 3's write to arrive late).
- *Animation:* without the fence and with reordering enabled, the final block reads `partial[3]` as stale (red "stale read"); with the fence, the write is visible before the ticket increments.
- *Aha moment:* the atomic ticket tells you *who is last*; only the fence guarantees *what they can see*.

## Check yourself
1. What does `__threadfence()` guarantee, and what does it not?
2. Why can spin-waiting on another block's flag deadlock?
3. How many global atomics does the last-block pattern issue for a grid of 1,000 blocks?

*PMPP reference:* Ch. 9 (atomic operations, throughput and contention, privatization), Ch. 11 (single-pass scan and inter-block coordination), Ch. 22 (advanced practices).

---

# APPEND TO D1: Global memory coalescing

## A general transaction formula
For one warp load, let *A* be the set of 32 byte-addresses and each access `w` bytes wide. Sectors fetched = number of distinct 32-byte-aligned sectors touched by any byte of any access.
$$\text{efficiency} = \frac{32 \cdot w}{32 \cdot \text{sectors}} = \frac{w \cdot 32}{\text{sectors} \times 32}$$
Stride-*s* float access (w = 4):
| Stride s (floats) | Span (bytes) | Sectors | Efficiency |
|---|---|---|---|
| 1 | 128 | 4 | 100% |
| 2 | 256 | 8 | 50% |
| 4 | 512 | 16 | 25% |
| 8 or more | ≥ 1,024 | 32 (one per lane) | 12.5% |
Efficiency never drops below 12.5% for 4-byte elements, because each lane costs at least one 32-byte sector. For 16-byte (`float4`) accesses the floor is 50%.

## Effective bandwidth under a bad pattern
A stride-4 kernel at 25% efficiency can use at most 0.25 × (η × 2,039 GB/s) ≈ **430 GB/s of useful data** on an A100 even though the memory system is saturated. Reports should print both "bytes moved" and "useful bytes".

## The transpose, quantitatively
Naive transpose of an N × N float matrix: reads coalesced, writes strided by N. Reads use 100% of their sectors; writes use 12.5%. Ideal traffic = 4N² (read) + 4N² (write) = 8N² bytes. Actual = 4N² (read at 100%) + 4N² ÷ 0.125 = 32N² (write at 12.5%) = 36N² bytes, so **4.5× more traffic than necessary**. The shared-memory tiled version (D4/D5) restores both sides to 100% and approaches the copy-kernel bandwidth.

## Check yourself (additional)
4. What is the lowest efficiency a 4-byte-element warp load can have?
5. Naive transpose moves how many times the ideal bytes?
6. Float4 access with stride 2 (in float4 units): efficiency?

*PMPP reference:* Ch. 6 (memory coalescing, corner turning, thread coarsening), Ch. 3/5 (row-major layout).

---

# APPEND TO D2: Roofline

## Arithmetic intensity worksheet (4-byte floats, DRAM bytes)
| Kernel | FLOPs per element/output | Bytes | AI (FLOP/B) |
|---|---|---|---|
| ReLU | 1 | 8 | 0.125 |
| Vector add | 1 | 12 | 0.083 |
| SAXPY | 2 | 12 | 0.167 |
| GEMV (y = A x, A streamed once) | 2 per matrix element | 4 per matrix element | **0.5** |
| Dot product | 2 | 8 | 0.25 |
| Softmax (row fits cache, 1 read + 1 write) | ~5 | 8 | ~0.6 |
| LayerNorm (same) | ~8 | 8 | ~1 |
| SpMV, CSR (E9) | 2 per nonzero | 12 per nonzero | 0.167 |
| 3×3 conv, direct, no reuse | 18 per output | 36+4 | ~0.45 |
| 3×3 conv, tiled with halo | 18 | ~4·1.27+4 | ~2 |
| Matmul, block tile B_M × B_N | 2 per K-step per output | 4(B_M+B_N)/(B_M·B_N) per K-step per output | **B_M·B_N / (2(B_M+B_N))** |
Matmul check: square tile T: T² ÷ (2·2T) = T/4 ✓. Tiles 32×32 → 8; 64×64 → 16; 128×128 → 32.

## Matmul AI vs the ridge (A100)
Ridge = 9.6 FLOP/B.
- Tiled with T = 16 → AI = 4: **memory-bound** (attainable 8.2 TFLOPS, 42% of peak).
- T = 32 → AI = 8: still memory-bound (attainable 16.3 TFLOPS, 84%).
- Compute-bound needs AI ≥ 9.6 ⇒ T/4 ≥ 9.6 ⇒ **T ≥ 38.4**. A 32×32 thread block cannot reach it; you need *register tiling / thread coarsening*, where each block tile is 64×64 or larger but fewer threads compute it (E7).

## Multiple compute ceilings
The roofline has several flat roofs: FP32 CUDA cores (19.5 TFLOPS on A100), TF32 tensor cores (156 TFLOPS *dense*), FP16/BF16 tensor cores (312 TFLOPS) *(spec)*. The ridge shifts right dramatically: 312 TFLOPS ÷ 2.039 TB/s ≈ **153 FLOP/B**, so a kernel at AI = 30 is compute-bound on the FP32 roof but **memory-bound** on the tensor-core roof. This is why large GEMMs need big tiles, multi-stage pipelines, and why elementwise epilogues (F3) matter once the matmul gets fast.

## 🎬 VIZ-ROOFLINE-LADDER (extension of VIZ-ROOFLINE)
- Add a **Roof selector** (FP32 / TF32 / FP16), a **Tile size** slider that moves the matmul dot along the roofline using `B_M·B_N/(2(B_M+B_N))`, and a "required tile for compute-bound" readout.

## Check yourself (additional)
4. AI of a dot product?
5. Required square tile size for compute-bound FP32 matmul on the T4 (ridge ≈ 25)?
6. Why does a faster roof make fusion more valuable?

*PMPP reference:* Ch. 5 (compute-to-global-memory-access ratio; the roofline idea appears in the Ch. 5 discussion of arithmetic intensity), Ch. 6 (performance checklist).

---

# APPEND TO D3: float vs float4

## Bytes in flight, quantified
One warp issuing `float` loads has 32 × 4 = 128 B in flight per load instruction; with `float4` it is 512 B. For the T4 case from A5 (25 × 128 B loads per SM needed):
- `float` loads: need 25 *independent* warp loads outstanding per SM.
- `float4` loads: need ≈ 7 (3.2 KB ÷ 512 B).
With 32 resident warps per SM (the T4 maximum, *(approx.)*), plain `float` already has enough if each warp keeps one load outstanding; **the advantage appears when occupancy is low or each warp serializes load → use → load.** Using `float4` is a cheap form of ILP.

## Instruction counts
For N = 2²⁶ elements: scalar needs N/32 = 2,097,152 warp-level load instructions; `float4` needs N/128 = 524,288. The kernel moves the same bytes; the saving is in issue slots, address arithmetic and L1 pressure.

## Tails with alignment
For N not divisible by 4: `N4 = N / 4` vector elements and `rem = N % 4` tail elements (0-3). N = 10,000,001 → 2,500,000 float4 + 1 tail. Use `(N4 + B - 1) / B` blocks for the vector part, and let the last few threads (or one extra thread) handle the tail with scalar code.

## Check yourself (additional)
4. N = 10,000,001, block 256: blocks for the float4 part?
5. Why can `float4` give *no* speed-up if the scalar kernel already reaches 85% of peak bandwidth?

*PMPP reference:* Ch. 6 (memory-bound kernels, coalescing, thread coarsening), Ch. 5 (memory scope).

---

# APPEND TO D4: Shared memory and tiling

## Why the naive tiled matmul is shared-memory-bound
Inner loop of the T×T tiled kernel, per `k`: each thread does 1 FMA and reads `As[ty][k]` and `Bs[k][tx]`.
- Per **warp** per `k`: `As[ty][k]` is one broadcast (1 shared load instruction, one cycle); `Bs[k][tx]` is 32 consecutive words (1 load instruction, one cycle). So **2 shared loads per 1 warp-FMA**.
- A100 SM: 128 B/cycle shared bandwidth = **1 warp-wide load per cycle**; FP32 peak = **2 warp-FMAs per cycle**.
- Cycle budget per warp-k: loads need 2 cycles; FMAs need 0.5 cycle. **Loads limit at 25% of FMA peak.**
This is why a *correct, tiled, barrier-synchronized* kernel typically reaches only a modest fraction of peak, and why register tiling (E7) is the next rung.

## Register tiling in numbers
Let each thread compute an `R × R` block of C in registers. Per `k` it loads R values of A and R of B from shared memory (2R loads) and does R² FMAs.
- Shared loads per warp-FMA = 2R / R² = 2/R.
- Balanced when load cycles ≤ FMA cycles: `2R ≤ R²/2` ⇒ **R ≥ 4**.
- Registers per thread ≈ R² accumulators + 2R operands + addressing ≈ 16 + 8 + ~16 = ~40 for R = 4.
Block tile with 16×16 threads of 4×4 each = **64 × 64** output tile → AI 16 FLOP/B (D2), above the A100 ridge of 9.6. **Both** bottlenecks (global bytes and shared bandwidth) are fixed by the same idea: more output per thread.

## Exact global-load accounting for edge tiles
M, N, K arbitrary, tile T. Tiles along K: `⌈K/T⌉`. Each block loads one A-tile and one B-tile per K-tile whether or not they hang off the edge (zero padded). So global load requests (in elements) = `⌈M/T⌉·⌈N/T⌉·⌈K/T⌉·2T²`. For M = N = K = 100, T = 16: tiles = 7 per dimension → 7³ · 512 = **175,616** elements loaded, vs the 2·100³/16 = 125,000 "ideal"; the 40% overhead is zero-padding waste. Choose T (or pad the matrix) so edge waste is small.

## Shared-memory capacity vs tile size
Bytes = 2·T²·4 (A and B tiles). T = 16 → 2 KB; T = 32 → 8 KB; 64×64 block tile with K-tile 16 → (64×16 + 16×64) × 4 = 8 KB. A100 allows up to 164 KB per SM, so shared memory is rarely the limiter for single-buffered tiles; double buffering doubles it.

## Check yourself (additional)
4. How many shared-memory loads per warp-FMA does a 4×4 register tile need?
5. M = N = K = 100, T = 16: how many tile-load elements are fetched in total?
6. Which resource does a bigger tile consume besides shared memory?

*PMPP reference:* Ch. 5 (tiled matrix multiplication, boundary checks, impact of memory usage on occupancy), Ch. 6 (thread coarsening).

---

# APPEND TO D5: Bank conflicts

## The general formula
For stride-*s* access `smem[s * lane]` on 4-byte words with 32 banks:
$$\text{conflict degree} = \gcd(s, 32)$$
| Stride s | gcd | Degree | Slowdown |
|---|---|---|---|
| 1 | 1 | none | 1× |
| 2 | 2 | 2-way | 2× |
| 3 | 1 | none | 1× |
| 4 | 4 | 4-way | 4× |
| 8 | 8 | 8-way | 8× |
| 16 | 16 | 16-way | 16× |
| 32 | 32 | 32-way | 32× |
| 33 | 1 | none | 1× |
Odd strides are conflict-free. That is exactly why padding a 32-wide row to 33 words works (column access has stride 33).

## 64-bit and wider accesses
For 8-byte (`double` / `float2`) accesses the hardware serves a half-warp per phase; the analysis uses 64-bit words with 16 effective banks per half-warp. Rule of thumb: stride-1 on any word size is conflict-free; for wider types verify with the profiler.

## Swizzling as an alternative to padding
Padding wastes `1/32` of the memory and breaks 16-byte alignment for vector loads. **XOR swizzling** stores element (r, c) at column `c ^ (r % 32)` so each row is permuted, keeping rows at power-of-two pitch. Conflict-free for both row and column access, and compatible with `float4`. (Used by high-performance GEMM kernels.)

## Scan's bank problem
Blelloch's strides double each level (E6): level *d* accesses `index·2^d`, giving up to 2^d-way conflicts. The standard fix: add `index >> 5` to every shared index (one pad word per 32).

## Check yourself (additional)
4. Conflict degree of `s[8*lane]`?
5. Why does an odd stride never conflict?
6. Name one advantage of swizzling over padding.

*PMPP reference:* Ch. 5 (shared memory), Ch. 6 (bank conflicts are covered under shared-memory performance considerations), Ch. 11 (scan and bank-conflict avoidance).

---

# APPEND TO D6: Registers, local, constant and read-only memory

## Register budget arithmetic
For 100% occupancy on the A100 at 256-thread blocks you need ≤ 32 registers/thread (table in B4). `__launch_bounds__(maxThreadsPerBlock, minBlocksPerSM)` asks the compiler to fit: `__launch_bounds__(256, 8)` ⇒ ≤ 65,536 ÷ (256×8) = **32 registers**. If the kernel genuinely needs 48, the compiler spills 16 values per thread to local memory. Each spill is a store and a later load: the extra DRAM/L1 traffic is `spilled values × threads × 4 B × 2`. For 1M threads and 16 spills that is 128 MB of unnecessary traffic.

## Reading `-Xptxas -v` output
Report fields to check: registers per thread, spill stores/loads (bytes), shared memory per block, constant memory. The simulator should print the same fields in the run report (F5).

## Constant memory broadcast arithmetic
Constant cache serves **one address per cycle** per SM *(approx.)*. If all 32 lanes read the same address: 1 cycle. If lanes read *d* distinct addresses: *d* cycles. A 5×5 filter (25 weights, same for all threads, read in the same order) is 25 broadcast reads ≈ 25 cycles per output, with no global traffic. Putting the same filter in global memory costs 25 cached loads per thread.

## Check yourself (additional)
4. A100: block 256, `__launch_bounds__(256, 6)`. Register cap per thread?
5. Constant-memory read where lane *i* reads `c[i]` (32 different addresses): cycles?

*PMPP reference:* Ch. 5 (constant memory, registers, local memory), Ch. 7 (constant memory for filters, tiled convolution).

---

# APPEND TO E1: Map kernels

## Choosing the grid-stride launch size
With block size B and a resident-block capacity C = SMs × blocksPerSM (from B4), launch **exactly C blocks** (or a small multiple) and loop. A100, B = 256, 8 blocks/SM → 864 blocks. Each thread then processes ≈ N / (864·256) elements: for N = 2²⁸ that is **1,214** elements, so launch overhead is amortized and wave quantization disappears. Trade-off: very small N under-fills the GPU; use `min(C, ⌈N/B⌉)`.

## Bytes and time for common maps (A100, η = 0.85, N = 2²⁶)
| Map | Bytes/elt | Total bytes | Time at 1,733 GB/s |
|---|---|---|---|
| ReLU / Sigmoid (in→out) | 8 | 537 MB | **0.31 ms** |
| Vector add | 12 | 805 MB | 0.46 ms |
| SAXPY | 12 | 805 MB | 0.46 ms |
| Dropout + mask output | 4 in + 4 out + 1 mask = 9 | 604 MB | 0.35 ms |
Sigmoid's `expf` is ~20-40 instructions but still ≪ memory time: 2²⁶ × 40 = 2.7 GFLOP ÷ 19.5 TFLOPS = 0.14 ms < 0.31 ms. Memory-bound still, but not by 75×: **transcendental-heavy maps can sit near the ridge**; check with the calculator (A5).

## Counter-based RNG (Dropout) in detail
Philox/SplitMix-style: `r = hash(seed, i)` produces 32 random bits per element with no state. Keep if `r < p_keep × 2³²`; scale by `1/p_keep`. Deterministic for a given (seed, i) regardless of how threads are scheduled, which is what makes tests reproducible and backward passes able to regenerate the mask instead of storing it (saves 1 B/elt of traffic).

## Check yourself (additional)
4. A100, block 256, 8 blocks/SM, N = 2²⁸: elements per thread in a grid-stride launch?
5. Why can the backward pass of Dropout avoid storing the mask?

*PMPP reference:* Ch. 2 (vector addition, kernel launch), Ch. 6 (coarsening/grid-stride patterns).

---

# APPEND TO E2: Reduction

## Cost model of the optimization ladder
Take N = 2²⁴ floats (64 MiB) on an A100; bytes read once = 67.1 MB.
- Ideal time: 67.1 MB ÷ (0.85 × 2,039 GB/s) = **39 µs**.
- Kernel launch ≈ 5 µs per kernel; a two-kernel reduction pays ≥ 10 µs of launch overhead; that is ~25% of the ideal time. Hence single-kernel last-block (C3) or atomics for final combine on small inputs.
- Blocks needed: if each thread loads 2 elements (ladder step 4), B = 256 → 2²⁴ / 512 = **32,768 blocks**. With grid-stride and each thread accumulating ~76 elements → 864 blocks (and a far shorter final stage).
Variant 1 (modulo indexing) wastes: at level *s*, only `1/(2s)` of lanes active, but **every** warp stays resident and divergent until s ≥ 32 → up to 3-5× slower than variant 3 in published step-by-step studies *(illustrative)*; verify with the simulator's lane-activity graph.

## Floating-point accumulation error
Sequential summation of N terms has worst-case relative error bound ≈ `(N−1)·u·Σ|x|`; a balanced tree gives ≈ `⌈log₂N⌉·u·Σ|x|` where u = 2⁻²⁴ ≈ 6×10⁻⁸ for FP32. Concrete failure: summing 10⁸ ones with one float accumulator **stops at 16,777,216 = 2²⁴**, because adding 1 to 2²⁴ rounds back to 2²⁴ (the spacing of floats there is 2). A tree reduction gets this right because each add combines similar-size partials.
Remedies: tree/pairwise (default on GPUs), Kahan compensation (extra registers), wider accumulators (FP64 or two-level FP32), or sort magnitudes (rarely worth it).

## Reduction latency-bound analysis for the last stages
The final 5 levels (warp) do 32 → 1 in 5 steps with ≤ 31 useful adds; with `__syncthreads()` each level costs ≈ barrier latency (tens of cycles); with shuffles each level ≈ shuffle latency (~25 cycles) without a barrier. For one block this is ≈ 5 × 25 = 125 cycles ≈ 0.09 µs: negligible per block but multiplied by 32,768 blocks it adds up unless the grid is right-sized.

## Check yourself (additional)
4. Why does the ones-sum stall at exactly 2²⁴?
5. N = 2²⁰, 256 threads, 2 elements per thread: blocks in stage 1? Elements entering stage 2?
6. Which scheme has the smaller worst-case error bound, sequential or pairwise?

*PMPP reference:* Ch. 10 (reduction trees, minimizing divergence, memory divergence, hierarchical reduction, thread coarsening).

---

# APPEND TO E3: Row-wise ops

## Does the row fit on-chip?
If a row of `C` floats fits in registers/shared memory (C ≲ 4K-8K floats per block in practice), load it **once** and do all three softmax passes on-chip: global bytes = 4C read + 4C write = 8C, which is already the lower bound. The online algorithm only matters when the row does **not** fit. Example: an LM-head softmax over a 50,257-token vocabulary = 201 KB per row, which exceeds the 164 KB shared memory on A100, so it needs the online (streaming) formulation (or splitting across a block + cluster).

## Online softmax: why the merge is correct
State (m, d) represents `d = Σ e^{x_j − m}` over the processed elements. Merge two states: with M = max(m₁, m₂),
$$d = d_1 e^{m_1 - M} + d_2 e^{m_2 - M}.$$
Each term rescales a sum "as if its max had been M", so the merged state equals the state you would get by processing all elements sequentially. Numeric check: (m₁,d₁) = (2,3) and (m₂,d₂) = (5,1) → M = 5, d = 3e⁻³ + 1 = 1.149.

## Welford and Chan's parallel merge for variance
Per-thread state (n, μ, M₂) with M₂ = Σ(x−μ)². Merge:
$$n = n_a+n_b,\quad \delta = \mu_b-\mu_a,\quad \mu = \mu_a + \delta\frac{n_b}{n},\quad M_2 = M_{2a}+M_{2b}+\delta^2\frac{n_a n_b}{n}.$$
Variance = M₂/n (or n−1). No catastrophic cancellation, and the same merge works at every level of the block tree. Show failure of the naive `E[x²]−E[x]²`: values 10⁸ + {1,2,3}: in FP32 the squares are ~10¹⁶ with spacing ~10⁹, so the variance computed this way is **garbage (often 0 or negative)** while the true variance is 2/3.

## Cross-entropy fused with softmax
Never materialize probabilities when you only need the loss: `loss = (m + log d) − z_t` from the online state. For a batch of 4,096 rows × 50,257 classes, skipping the probability matrix saves 823 MB of writes and reads per pass (4,096 × 50,257 × 4 B ≈ 823 MB).

## Check yourself (additional)
4. Bytes moved by a row-resident softmax of C = 4,096 floats (per row)?
5. Chan-merge two groups: (n=2, μ=1, M₂=2) and (n=2, μ=5, M₂=2). Result?
6. Why is fusing cross-entropy with softmax a memory win?

*PMPP reference:* Ch. 10 (reduction patterns used inside row-wise kernels), Ch. 16 (deep learning kernels: softmax, normalization as used in networks). *Online softmax / FlashAttention: not in PMPP; cite Milakov & Gimelshein (2018) and Dao et al. (2022) in "Further reading".*

---

# APPEND TO E4: Stencils and convolution

## FLOP and byte counting for direct convolution
For a conv layer with batch N, input channels C_in, output channels C_out, output size H × W, kernel K × K:
$$\text{FLOPs} = 2\cdot N\cdot C_{out}\cdot H\cdot W\cdot C_{in}\cdot K^2$$
Example: N = 32, C_in = 64, C_out = 128, H = W = 56, K = 3 → 2 · 32 · 128 · 3,136 · 64 · 9 = **14.8 GFLOP**. Input = 32·64·56·56·4 B = 25.7 MB; output = 32·128·3,136·4 B = 51.4 MB; weights = 128·64·9·4 = 295 KB. Ideal bytes ≈ 77 MB → AI ≈ **192 FLOP/B**: strongly compute-bound *if* data reuse is perfect, which is why convolutions are implemented as GEMM or with large register tiles.

## Convolution as GEMM (im2col)
Build a matrix of shape (N·H·W) × (C_in·K²) = 100,352 × 576 (4 B each = **231 MB**, i.e. 9× the input) and multiply by a (C_in·K²) × C_out filter matrix. The GEMM then reaches high AI but the im2col buffer costs memory traffic. **Implicit GEMM** forms the tiles on the fly inside the kernel from the original tensor, avoiding the 231 MB buffer (the basis of cuDNN-style kernels). Winograd and FFT trade multiplications for additions/transforms for small/large K respectively *(context only)*.

## Separable filters
A K × K filter that factors as an outer product `a bᵀ` can be applied as two 1D passes: MACs per output **2K instead of K²** (3×3: 6 vs 9; 7×7: 14 vs 49). Gaussian blur and many classical filters are separable; learned conv filters generally are not.

## Halo overhead formula
2D tile T_x × T_y with an (K−1)/2 halo: loads per output = (T_x+K−1)(T_y+K−1)/(T_x·T_y). 16×16 with K = 3: 324/256 = 1.27; K = 5: 400/256 = 1.56; K = 7: 484/256 = 1.89. 3D tile 8×8×8 with K = 3: 10³/8³ = **1.95**; K = 5: 12³/512 = 3.4 (why 3D tiles suffer).

## Check yourself (additional)
4. FLOPs of a 1×1 convolution with C_in = C_out = 256 on a 14 × 14 map, batch 1?
5. Halo overhead (loads per output) for K = 5, tile 16 × 16?
6. Why can't a stride-2 2×2 max-pool use shared-memory tiling profitably?

*PMPP reference:* Ch. 7 (convolution: constant memory for filters, tiled convolution with halo cells, caching of halo cells in L2), Ch. 8 (stencil: 3D tiling, thread coarsening, register tiling), Ch. 16 (convolutional layers as matrix multiplication: im2col).

---

# APPEND TO E5: Histogram and atomics

## Counting atomics precisely
- **Naive global:** one global atomic per input element: N operations (N = 2²⁴ ⇒ 16.8 M).
- **Privatized, per-block histogram:** per block, `elements_per_block` shared atomics plus up to `bins` global atomics for the merge. Global atomics = `blocks × bins`. 128 blocks × 1,024 bins = **131,072** (128× fewer than naive for N = 2²⁴).
- **Capacity limit:** bins × 4 B ≤ shared per block: 164 KB → ≈ 41,000 bins max on an A100 (fewer if other shared use). Above that, privatize into **global** per-block copies or use multi-pass binning.

## Contention model (illustrative)
Let a fraction *f* of all inputs hit the hottest bin and same-address atomics complete at roughly one per ~1 ns: serialized time ≈ f·N ns. N = 2²⁶, f = 0.9 → 60 ms; uniform data → throughput-limited ≈ memory time (~0.1-0.3 ms). Privatization moves the hot-bin serialization to shared memory (much faster and independent per block).

## Warp-aggregated atomics
When many lanes in a warp hit the *same* bin, combine them first: `mask = __match_any_sync(full, bin)`; the lane with the lowest id in the mask is the *leader*; it adds `__popc(mask)` in one atomic. Cost: a couple of warp intrinsics; benefit: up to 32× fewer atomics on skewed data. The same trick gives *stream compaction* offsets: `rank = __popc(mask & lanemask_lt)`.

## Interleaved vs contiguous coarsening
When each thread handles several inputs, assign them with **stride = total threads** (interleaved), not contiguous chunks, so a warp's loads at each step are coalesced (D1).

## Check yourself (additional)
4. 128 blocks, 1,024 bins: global atomics for the merge?
5. How does `__popc(mask)` reduce atomics on skewed data?
6. Why interleaved rather than contiguous per-thread chunks?

*PMPP reference:* Ch. 9 (atomics, latency/throughput, privatization, coarsening, interleaved partitioning, aggregation).

---

# APPEND TO E6: Prefix sum

## Work and depth: exact counts
| Algorithm | Depth (steps) | Additions |
|---|---|---|
| Sequential | N−1 | N−1 |
| Hillis-Steele (inclusive) | log₂N | N·log₂N − (N−1) |
| Blelloch (exclusive) | 2·log₂N | 2(N−1) |
| Brent-Kung (inclusive) | 2·log₂N − 1 | 2N − 2 − log₂N |
N = 8: 17 / 14 / 11. N = 256: Hillis-Steele **1,793**, Blelloch **510**. N = 1,024: 9,217 vs 2,046 (4.5×). With *p* processors you cannot exploit the depth win if work is high: work-efficient algorithms win once N ≫ p, which is the usual GPU regime.

## Multi-block scan memory traffic
- **Scan-then-propagate:** pass 1 reads N and writes N (partial scans) plus the block sums; the block sums are scanned; pass 2 reads N and writes N (adding offsets). Total **4N words** moved. A "reduce-then-scan" variant has pass 1 only compute block sums (read N, write ~0) and pass 2 do the scan and offset in one go (read N, write N): **3N words**.
- **Decoupled look-back (single pass):** each block publishes its aggregate and reads predecessors' *inclusive prefixes* with flags; reads N, writes N = **2N words**: about **1.5-2× less traffic**, and the scan reaches the speed of a copy. (Merrill & Garland, 2016: not in PMPP; PMPP covers the hierarchical and single-pass/domino-style variants in Ch. 11.) Forward progress relies on blocks being scheduled in order (a block only waits on lower-numbered blocks), an exception to "never wait for other blocks" that is safe by construction.

## Compaction example
Input `[5, 0, 7, 0, 0, 3]`, predicate `x != 0` ⇒ flags `[1,0,1,0,0,1]`; exclusive scan `[0,1,1,2,2,2]`; survivors write to those positions: `out[0]=5, out[1]=7, out[2]=3`; count = last scan + last flag = 3.

## Bank-conflict-free indexing
`#define OFFSET(i) ((i) + ((i) >> 5))` on every shared-memory index in the up-/down-sweep, with the array sized `N + N/32`.

## Check yourself (additional)
4. Hillis-Steele additions for N = 16?
5. Compaction of `[2, 9, 0, 4, 0, 0, 6]` keeping nonzeros: scan and output?
6. Why is decoupled look-back "safe" despite inter-block waiting?

*PMPP reference:* Ch. 11 (Kogge-Stone [≈ Hillis-Steele], Brent-Kung, coarsening, segmented/hierarchical scan, single-pass scan), Ch. 9 (compaction relates to histogram-style output positioning).

---

# APPEND TO E7: The matmul ladder

## The full cost table (A100, N = M = K = 4096, FP32 CUDA cores)
Total work: 2·4096³ = **137.4 GFLOP**. Compute floor at η_c = 0.8: 137.4 ÷ (0.8 × 19.5 T) = **8.8 ms** (7.05 ms at peak). Ideal DRAM bytes (A, B in, C out once): 3 × 4096² × 4 = 201 MB ⇒ 0.10 ms. DRAM-limited times are bytes ÷ 1.733 TB/s (η = 0.85).
| Version | Block tile | AI (FLOP/B) | Global bytes (no-cache model) | Memory time | Bound |
|---|---|---|---|---|---|
| v1 naive | 1×1 | 0.25 | 550 GB | **317 ms** | memory |
| v3 tiled T=16 | 16×16 | 4 | 34.4 GB | 19.8 ms | memory |
| v3 tiled T=32 | 32×32 | 8 | 17.2 GB | 9.9 ms | memory (just) |
| v6 register tile | 64×64 | 16 | 8.6 GB | 5.0 ms | **compute** |
| v6 register tile | 128×128 | 32 | 4.3 GB | 2.5 ms | compute |
*Caveat:* the "no-cache model" overstates v1 because L1/L2 catch some of the reuse; real naive kernels run perhaps an order of magnitude better than 317 ms but still far from the tiled versions. Label this column "model upper bound" in the viz. The ladder's key insight: **T = 32 is *still* memory-bound on the A100**; only the 64×64 block tile (v6) crosses the ridge.

## Why v2 (the coalescing fix) matters even though loads per output are unchanged
v1 with `x → row`: a warp's 32 lanes read `B[k][col]` at 32 different rows → 32 sectors per load, stride-N access (12.5%). With `x → col`: `B[k][col..col+31]` is one 128 B line (100%). Same arithmetic, same load *count*, up to 8× fewer bytes moved.

## Vectorized and double-buffered versions
- v5: `float4` global → shared loads cut load-instruction counts by 4 (D3).
- v7 (concept): with multi-stage pipelines the load of tile *k+1* overlaps compute on tile *k* (asynchronous copies on Ampere+). Time per K-step ≈ max(load, compute) instead of the sum. If load = 60% and compute = 100% of equal units, the sum is 1.6; the max is 1.0, a **1.6×** upper bound on gain.

## Tensor cores in numbers *(spec; context)*
A100 TF32: 156 TFLOPS dense; FP16/BF16: 312 TFLOPS: roughly 8× and 16× the FP32 roof. At that speed even 128×128 tiles sit left of the ridge: with 2-byte FP16 operands the AI is `B_M·B_N / (B_M+B_N)` = 64 FLOP/B, versus a ridge of about 153 FLOP/B, so real kernels use bigger tiles (128×256), deep pipelines, and rely on L2 reuse. The simulator does not model tensor cores.

## Check yourself (additional)
4. AI of a 64 × 128 block tile?
5. Memory time (η = 0.85) of v3 with T = 16 at N = 4096 on A100?
6. Why does a faster compute roof make bandwidth-optimization matter more?

*PMPP reference:* Ch. 5 (tiled GEMM, the core derivation), Ch. 6 (corner turning, thread coarsening), Ch. 16 (GEMM in deep learning); register tiling and software pipelining are discussed across Ch. 6 and 22. *Tensor cores: not in PMPP's main text; cite vendor architecture whitepapers.*

---

# APPEND TO E8: Sorting day

## Counting comparators and bytes
- **Bitonic**, N = 2^k: stages k(k+1)/2, N/2 comparators each ⇒ `N/2 · k(k+1)/2`. N = 1,024 ⇒ 512 × 55 = **28,160** compare-exchanges, vs the information-theoretic ≈ N log₂N = 10,240 (2.75×). N = 2²⁰ ⇒ 20·21/2 = 210 stages × 524,288 = 110 M comparators. With data in shared memory for the first ~log₂(B) stages only the later stages touch global memory.
- **LSD radix sort**, 32-bit keys, *r* bits per pass ⇒ ⌈32/r⌉ passes. r = 8 ⇒ 4 passes; each pass reads and writes the keys once (+ histogram/scan overhead): ≈ 8 B × N per pass. N = 2²⁶ (67 M keys): 4 passes × 537 MB = 2.1 GB ⇒ **≈ 1.2 ms** at 1.73 TB/s *(lower bound; real sorts add scan traffic and reach perhaps 50-70% of that rate)*. Larger *r* ⇒ fewer passes but bigger histograms (2^r bins); 4-8 bits is typical.

## Radix pass step by step
For the current digit: (1) per-block histogram of digit values; (2) exclusive scan over the (digit, block) matrix gives each (block, digit) its global output offset; (3) each element's destination = offset[digit] + its rank among same-digit elements in the block; (4) scatter. Stability (keeping order within equal digits) is what makes successive digit passes compose into a sorted order.

## Merge path (balanced merging)
To merge sorted arrays A and B with *p* workers, find for each worker the split `(i, j)` with `i + j = k·(|A|+|B|)/p` that partitions the merged output evenly: a **co-rank** binary search of O(log N) per worker. Every worker then merges an equal-sized output slice, avoiding the load imbalance of naive partitioning.

## Zero-one principle
A comparator network sorts all inputs iff it sorts all 0/1 inputs. That is the proof behind "the same wiring sorts any input" (check yourself #1 of E8).

## Check yourself (additional)
4. Compare-exchange count of bitonic sort for N = 64?
5. Radix passes for 64-bit keys with 8-bit digits?
6. Why must a radix pass be stable?

*PMPP reference:* Ch. 12 (merge: co-rank function, parallel merge, tiled merge), Ch. 13 (sorting: radix sort, parallel radix, coalescing optimizations, merge sort), Ch. 11 (scan used inside radix sort).

---

# NEW CHAPTER E9: Sparse matrices and SpMV
`id: E9 · part: E · est: 35 min · prereqs: C1, D1, D2, E2 · problems: proposed CU-053 · pmpp: Ch. 14`

## Why sparse
A matrix with mostly zeros (graphs, finite elements, pruned networks) wastes memory and time if stored densely. Store only the nonzeros plus their positions, and write kernels whose access patterns follow the data.

## Formats and their GPU personalities
Take the 4×4 matrix with rows `[5 0 0 1]`, `[0 2 0 0]`, `[0 0 0 0]`, `[3 0 4 6]`.
| Format | Stored | Strength | Weakness |
|---|---|---|---|
| **COO** (coordinate) | (row, col, val) per nonzero | simple, order-free | 12 B/nnz, needs atomics or segmented reduction |
| **CSR** (compressed sparse row) | `val[]`, `col[]`, `rowptr[]` | compact (≈ 8 B/nnz + 4 B/row), row access fast | rows have varying length ⇒ imbalance, divergence |
| **ELL** (ELLPACK) | each row padded to the max row length, stored **column-major** | perfectly regular, coalesced | padding waste when row lengths vary |
| **HYB / hybrid** | ELL for the regular part + COO for overflow | balances regularity and waste | more complex |
CSR here: `val=[5,1,2,3,4,6]`, `col=[0,3,1,0,2,3]`, `rowptr=[0,2,3,3,6]`. Row *r* occupies `val[rowptr[r] .. rowptr[r+1]−1]`.

## SpMV (y = A x) mappings
1. **One thread per row (CSR scalar):** simple; adjacent threads read `val` at addresses separated by their row lengths ⇒ **uncoalesced**, and a warp runs as long as its **longest** row (loop divergence, C1).
2. **One warp per row (CSR vector):** the 32 lanes stride across the row (coalesced loads of `val`, `col`), then warp-shuffle reduce (F1). Good for rows ≳ 32 nonzeros; wasteful for short rows (most lanes idle).
3. **ELL:** thread per row, column-major storage ⇒ at each step adjacent threads read adjacent addresses ⇒ perfectly coalesced.
4. **Merge-based / nonzero-split:** assign equal numbers of nonzeros to each thread block, then fix row boundaries with a co-rank-style search (E8); load-balanced for any row-length distribution.

## Arithmetic intensity and the roofline
Per nonzero: 2 FLOPs (multiply + add); bytes ≈ 4 (val) + 4 (col) + 4 (gather of `x[col]`, assuming cache misses) = **12 B ⇒ AI ≈ 0.17 FLOP/B**. On an A100 the roofline ceiling is 0.167 × 2,039 ≈ **340 GFLOP/s, 1.7% of the 19.5 TFLOPS peak**. SpMV is the canonical memory-bound, irregular kernel: only fewer bytes (better formats, caching `x`, smaller index types, reordering for locality) help. Gather accesses `x[col]` are uncoalesced; reordering rows/columns (e.g., reverse Cuthill-McKee) improves cache hits.

## Padding cost in ELL
Waste = (rows × max_len − nnz) / (rows × max_len). If 1,000 rows have lengths with mean 8 but one row has 500, ELL stores 500,000 slots for 8,492 nonzeros: **98% waste**, which is why HYB exists.

## 🎬 VIZ-SPMV-FORMATS: "Same matrix, four layouts"
- *Canvas:* a 16 × 16 sparse matrix (editable sparsity pattern or presets: banded, random, one dense row, power-law). Beside it, memory strips for COO, CSR, ELL.
- *Controls:* **Format**, **Mapping** (thread-per-row / warp-per-row), **Row-length distribution**, `Stepper`.
- *Animation:* for thread-per-row a `LaneStrip` shows lanes dropping out as short rows finish (divergence) while the longest row keeps the warp busy; for warp-per-row all lanes stay active on long rows but idle on short rows. Memory strip shows the addresses touched at each step, sectors lit as in VIZ-COALESCING.
- *Readouts:* **lane utilization %**, **sectors per load**, **padding waste %**, **bytes/nnz**.
- *Aha moment:* with one huge row, ELL wastes memory, scalar-CSR stalls a warp, and only nonzero-splitting stays balanced.

## Check yourself
1. Write the CSR arrays for the matrix `[[0,2,0],[1,0,3],[0,0,0]]`.
2. Rows have 1-4 nonzeros. Better mapping: thread-per-row or warp-per-row? Why?
3. Why is SpMV stuck below 2% of peak FLOPs?

## Pitfalls
- Using `int` row pointers when nnz > 2³¹.
- Ignoring the output `y` writes and `rowptr` reads when counting bytes.

## Proposed problem
**CU-053 SpMV (CSR)**: implement thread-per-row, then warp-per-row; report shows sectors per load and lane utilization.

*PMPP reference:* Ch. 14 (sparse matrix computation: COO, CSR, ELL, hybrid, JDS and their SpMV kernels; control divergence and memory divergence trade-offs).

---

# NEW CHAPTER E10: Graph traversal (BFS)
`id: E10 · part: E · est: 30 min · prereqs: E5, E6, C1 · problems: proposed CU-054 · pmpp: Ch. 15`

## The problem
Breadth-first search computes the distance (in edges) from a source vertex to every other vertex. It is **irregular** (the amount of work per level depends on the graph), **data-dependent** (memory addresses come from edge lists), and **low-arithmetic** (almost pure memory traffic).

## Level-synchronous BFS
Maintain a **frontier** (vertices discovered at the current level). Each iteration visits every neighbour of every frontier vertex; unvisited neighbours join the next frontier. One kernel launch per level; the launch boundary is the global barrier that blocks cannot provide themselves (B2).

## Parallelization choices
1. **Vertex-centric, push:** one thread per *frontier vertex* iterates over its edges, marking neighbours with `atomicCAS(&dist[v], INF, level+1)` so each vertex is claimed once. Imbalance: a high-degree vertex's thread runs long (loop divergence, C1).
2. **Vertex-centric, pull (bottom-up):** one thread per *unvisited* vertex scans its neighbours looking for **any** frontier member and stops at the first hit. Much cheaper when the frontier is huge (most vertices are about to be visited).
3. **Edge-centric:** one thread per edge; perfectly balanced work but scans all edges every level (wasteful in early/late levels).
4. **Direction-optimizing:** push while the frontier is small, pull when it is large: a standard choice in modern GPU BFS.

## Building the next frontier
Threads append discovered vertices to a shared queue. Contended `atomicAdd` on one tail pointer is a hotspot; use **block-local queues** (shared-memory counters, privatization from E5) and a block-level merge, or **warp-aggregated** appends (E5). With scan (E6) you can compute exact write offsets without atomics on the queue.

## The numbers
Per edge traversed: read the neighbour id (4 B, coalescable within an adjacency list), read/CAS `dist[v]` (random 4 B access = a full 32 B sector, 12.5% efficient). So ≈ 4 + 32 = **~36 B moved per edge** for ≈ 1 useful operation. A graph with 10⁹ edges ⇒ ≈ 36 GB ⇒ ≈ 21 ms at 1.7 TB/s *(lower bound for a single full-graph sweep)*. Graph analytics performance is measured in **TEPS** (traversed edges per second); the bandwidth model above caps it near 10¹⁰ TEPS on an A100 *(illustrative)*.

## Why graphs are hard on GPUs
Power-law degree distributions (a few vertices with millions of edges), random memory access (no coalescing), and frontier sizes that vary by orders of magnitude between levels. The remedy theme is the same as everywhere: sort/bucket by degree, cooperate across lanes (warp- or block-per-vertex for heavy vertices), and keep the frontier compact.

## 🎬 VIZ-BFS-FRONTIER: "Level by level"
- *Canvas:* a graph (up to 40 nodes; presets: grid, random, star-with-hub, power-law) with nodes coloured by level; below it a bar chart of **frontier size per level** and a `LaneStrip` showing which lanes own frontier vertices.
- *Controls:* **Strategy** (push / pull / direction-optimizing), `Stepper`, **Source vertex**.
- *Readouts:* **edges examined per level**, **atomic claims**, **lane utilization**.
- *Aha moment:* on the hub graph, push explodes at one level (one thread does all the work) while pull examines far fewer edges at the big middle level.

## Check yourself
1. Why must `dist[v]` be claimed atomically in push-style BFS?
2. When is bottom-up (pull) cheaper than top-down?
3. Why is one kernel launch per BFS level a natural fit for level-synchronous BFS?

## Proposed problem
**CU-054 BFS (level-synchronous, push)**: report shows atomics, lane utilization, bytes per edge.

*PMPP reference:* Ch. 15 (graph traversal: vertex-centric push/pull, edge-centric, frontier-based, privatization of frontiers, load balancing).

---

# APPEND TO F1: Warp-level primitives

## Counting the savings
Reducing 256 values with shared memory only: log₂256 = 8 levels, **8 barriers**, ~8 × (shared load + add + store). With shuffles for the within-warp levels: 5 shuffle levels + 1 shared exchange + 3 shuffle levels, **1 barrier**. Per block this removes 7 barriers and cuts shared-memory traffic from 255 reads + 255 writes to 8 reads + 8 writes.

## Block reduction recipe
1. Each warp reduces its own 32 values with `__shfl_down_sync` (5 steps).
2. Lane 0 of each warp writes its result to `smem[warp_id]` (≤ 32 slots).
3. `__syncthreads()`.
4. Warp 0 loads `smem[lane]` (pad lanes ≥ #warps with the identity element), reduces again with shuffles.
5. Thread 0 owns the block result.

## Voting for compaction and aggregation
- `ballot = __ballot_sync(full, pred)`; `count = __popc(ballot)`; `rank = __popc(ballot & ((1u << lane) - 1))`.
- Leader election: `leader = __ffs(ballot) - 1`.
- Warp-aggregated atomic (E5, E10): the leader does one `atomicAdd(&tail, count)` and broadcasts the base with `__shfl_sync`; each active lane writes at `base + rank`.

## What `shfl_down` returns at the edge
For `__shfl_down_sync(mask, v, delta)`, lane *i* with `i + delta ≥ 32` receives **its own** `v` (not zero). Reductions must be written so those lanes' results are ignored or harmless (they only matter for lane 0's final answer, which is unaffected).

## Check yourself (additional)
4. Barriers per block for a shuffle-based reduction of 256 threads?
5. Given `ballot = 0b1011_0100` and lane = 5, what is `rank`?

*PMPP reference:* Ch. 10 (reduction hierarchy; warp-level shuffle variants appear in later editions' optimizations and in Ch. 22 "advanced practices"), Ch. 9 (aggregation).

---

# APPEND TO F2: Streams and overlap

## The pipeline time formula
Split work into *S* equal chunks. Per-chunk times: copy-in h = H/S, compute k = K/S, copy-out d = D/S. With enough engines and ideal overlap:
$$T(S) \approx (h + k + d) + (S-1)\cdot\max(h, k, d)$$
(first chunk fills the pipeline, then one chunk completes every max(·).)
Example: H = D = 40 ms, K = 10 ms, S = 4: h = d = 10, k = 2.5 ⇒ T = 22.5 + 3 × 10 = **52.5 ms** vs 90 ms serial (1.7×). Lower bound = max(H, K, D) = 40 ms. As S → ∞ the formula approaches 40 ms plus per-chunk overheads. Each extra chunk adds launch/sync overhead (~10-20 µs), so there is a sweet spot (often 4-16 chunks).
Note: H2D and D2H use separate copy engines on most data-center GPUs, but both share the PCIe link's *directional* bandwidth only with their own direction, so full-duplex overlap of in/out is realistic; with only one copy engine the in/out copies serialize and the formula's `max` becomes `max(h + d, k)`.

## Which stream rules matter
- Same stream ⇒ ordered; different streams ⇒ no order unless you add events (`cudaEventRecord` / `cudaStreamWaitEvent`).
- The default stream has legacy synchronizing behaviour unless you use per-thread default streams.
- Pageable memory is staged through a pinned buffer by the driver, so the copy cannot be fully asynchronous.

## Check yourself (additional)
3. H = D = 60 ms, K = 20 ms, S = 6: T(S)?
4. What changes if the GPU has one copy engine?

*PMPP reference:* Ch. 20 (CUDA streams, overlapping data transfer and computation in the heterogeneous-cluster chapter), Ch. 22 (advanced practices; asynchronous operations).

---

# APPEND TO F3: Fusion and attention

## Exact traffic for standard vs fused attention (one head, FP32)
N = 4,096, head dimension d = 64. Sizes: Q, K, V, O each N × d × 4 B = **1.05 MB**; S = N × N × 4 B = **67.1 MB** (the original text rounds to 64 MB; use 67.1 MB or 64 MiB).
Standard (3 kernels): write S (67.1) + read S for softmax (67.1) + write P (67.1) + read P for P·V (67.1) = **268 MB** of S/P traffic, plus 4.2 MB for Q, K, V, O ≈ 273 MB ⇒ 0.16 ms at 1.73 TB/s per head per sequence (and ×heads ×batch).
Memory footprint is O(N²): doubling N quadruples it (N = 16,384 ⇒ 1.07 GB per head).

## FlashAttention-style tiling accounting
Block of Q rows (B_r) stays in shared/registers; K, V stream in tiles of B_c rows. On-chip need: Q_i, O_i (B_r × d each), K_j, V_j (B_c × d each) + score tile (B_r × B_c). With B_r = B_c = 64, d = 64, FP32: 4 × 64 × 64 × 4 B = 64 KB + 16 KB = **80 KB**, which fits in 164 KB.
Global traffic: Q, O once (2.1 MB); K, V are re-read once per Q-block: N/B_r = 64 times × 2.1 MB = 134 MB ⇒ about **138 MB** if every re-read misses L2 (about 2× less than standard); at B_r = 128 it is ≈ 70 MB. In practice K, V (2.1 MB per head) are **L2-resident** across Q-blocks, so DRAM traffic approaches ≈ 4.2 MB. The *definite* win is the O(N) rather than O(N²) memory footprint, which makes long sequences possible.
Each tile update merges online-softmax state exactly as in E3:
$$m' = \max(m, \text{rowmax}(S_{ij})),\quad d' = d\,e^{m-m'} + \text{rowsum}(e^{S_{ij}-m'}),\quad O' = O\,\frac{d\,e^{m-m'}}{d'} + \frac{e^{S_{ij}-m'}V_j}{d'}$$
(implementations usually defer the division by *d′* to the very end and track the un-normalized output).

## When fusion saves time and when it barely does (calculation)
A concrete case: the MLP block of F6 (M = 2,048 tokens, d = 1,024, hidden h = 4,096, FP32, A100).
- FLOPs: 4·M·d·h = **34.4 GFLOP** ⇒ at 80% of 19.5 TFLOPS = **2.2 ms**; ≈ 1.76 ms at peak.
- Separate elementwise kernels (bias+GELU on h = 33.5 MB; bias+residual on y = 8.4 MB) add ≈ **176 MB** of traffic ⇒ **≈ 0.10 ms** at η = 0.85, about 5% of the matmul time on FP32 cores. *Fusion is a small win here.*
- With TF32 tensor cores (156 TFLOPS peak ⇒ ≈ 0.28 ms at 80%), the same 0.10 ms is **≈ 36%**. *Fusion is a big win.*
Moral: fusion's value scales with how fast the neighbouring compute is and how memory-bound the elementwise part is. Always put numbers on it (A5).

## Check yourself (additional)
4. S-matrix size (FP32) for N = 8,192?
5. On-chip bytes for Flash tiles with B_r = B_c = 128, d = 64, FP32? Does it fit in 164 KB?
6. When is fusing a bias + GELU epilogue a < 10% win?

*PMPP reference:* Ch. 16 (deep learning: fused operations context), Ch. 5-6 (tiling). **Not in PMPP:** FlashAttention itself (Dao et al., 2022) and online softmax (Milakov & Gimelshein, 2018).

---

# APPEND TO F4: Multi-GPU and NCCL

## The α-β cost model
Time to send *n* bytes over one link: `T = α + n/β` with latency α (≈ 5-10 µs) and bandwidth β.
- **Ring AllReduce**, *p* GPUs, data size D:
$$T_{\text{ring}} = 2(p-1)\,\alpha + 2\,\frac{p-1}{p}\cdot\frac{D}{\beta}$$
- **Tree AllReduce** (reduce up + broadcast down, double-binary-tree in NCCL):
$$T_{\text{tree}} \approx 2\log_2 p\cdot\alpha + c\cdot\frac{D}{\beta}$$
Ring is **bandwidth-optimal** (volume factor → 2 as p grows, not growing with p) but has latency growing linearly with p; trees have latency O(log p). Small messages ⇒ tree/latency-optimized; large messages ⇒ ring/bandwidth-optimized. NCCL picks automatically.

## Worked example: gradients of a 250 M-parameter model (FP32 ⇒ D = 1 GB)
- **8 GPUs, NVLink**, β = 300 GB/s per direction *(A100 NVLink3 ≈ 600 GB/s bidirectional)*: bandwidth term = 2 × (7/8) × 1 GB ÷ 300 GB/s = **5.8 ms**; latency term = 14 × 5 µs = 0.07 ms ⇒ **≈ 5.9 ms**.
- **8 GPUs over PCIe 4.0** (β ≈ 25 GB/s through the host/switch): 1.75 GB ÷ 25 GB/s = **70 ms**: 12× slower.
- **Per-GPU bytes sent** with p = 2: D; p = 8: 1.75 D; p = 64: 1.97 D; p → ∞: 2 D (**nearly constant**).
If the backward pass takes 100 ms, a 5.9 ms AllReduce can be **fully overlapped** (gradient buckets are reduced as soon as they are ready, while earlier layers are still computing), whereas 70 ms cannot be hidden entirely.

## Reduce-scatter and all-gather separately
ReduceScatter + AllGather = AllReduce. Sharded optimizers (ZeRO / FSDP) keep gradients and optimizer state **sharded** and use only ReduceScatter then AllGather of *parameters* when needed, trading extra communication steps for memory. Volume per GPU: ReduceScatter ≈ (p−1)/p · D, AllGather ≈ (p−1)/p · D.

## Parallelism flavours in one table
| Scheme | What is split | Communication |
|---|---|---|
| Data parallel | batch | AllReduce of gradients |
| Tensor parallel | each weight matrix (columns/rows) | AllReduce/AllGather of activations *inside* every layer (needs NVLink-class bandwidth) |
| Pipeline parallel | layers into stages | point-to-point activations between stages; bubbles |
| Sharded data parallel (FSDP/ZeRO) | params/grads/optimizer state | AllGather + ReduceScatter |

## Check yourself (additional)
4. Ring AllReduce time for D = 400 MB, p = 4, β = 50 GB/s (ignore latency)?
5. Why do tensor-parallel layers need faster links than data-parallel gradient sync?
6. Which two collectives compose into an AllReduce?

*PMPP reference:* Ch. 20 (programming a heterogeneous cluster: MPI, halo exchange, overlapping communication and computation, CUDA-aware MPI). **Not in PMPP:** NCCL's ring/tree implementation details and FSDP/ZeRO: cite NCCL docs and the ZeRO paper.

---

# APPEND TO F5: Debugging and the profiling mindset

## A checklist of numbers to read from any report
| Number | Healthy | Suspicious | Chapter |
|---|---|---|---|
| Global load efficiency | ~100% | < 50% | D1 |
| Bytes moved ÷ lower bound | ≈ 1-1.3 | > 2 | D2 |
| Bank-conflict cycles | 0 | > 0 on hot loops | D5 |
| Lane utilization / divergence | ~100% | < 70% in the main loop | C1 |
| Occupancy & limiter | matches the kernel's latency needs | limiter = registers with spills | B4, D6 |
| % of roofline | > 70% | < 30% | D2 |
| Register spills | 0 | > 0 | D6 |

## Compute-sanitizer family
`memcheck` (out-of-bounds, misaligned access, leaks), `racecheck` (shared-memory hazards RAW/WAR/WAW), `synccheck` (barrier misuse, divergent `__syncthreads`), `initcheck` (reads of uninitialized global memory). The simulator's four diagnostic classes correspond one-to-one.

## Determinism checklist
Run the same input 10 times: results must be bitwise-identical unless you intentionally use atomics/unordered reductions. If they differ: (1) race, (2) uninitialized memory, (3) float atomics ordering, (4) `__syncthreads()` missing, (5) out-of-bounds read of a neighbouring allocation.

## Timing correctly
Use CUDA events (`cudaEventRecord` before/after, `cudaEventElapsedTime`), **warm up** (first launch includes context/JIT costs), run ≥ 10 iterations, report the **median**, and synchronize before stopping the clock (A2/B5). Compare against the copy-kernel bandwidth (A4) for memory-bound kernels.

## Check yourself (additional)
3. A kernel's global load efficiency is 25% and its bank conflicts are zero. Which chapter do you open first?
4. Why must you warm up before timing?

*PMPP reference:* Ch. 6 (performance checklist and tuning strategies), Ch. 22 (profiling and tooling context).

---

# NEW CHAPTER F7: Launch overhead, CUDA graphs and dynamic parallelism
`id: F7 · part: F · est: 25 min · prereqs: B5, F2 · problems: theory + calculation quiz · pmpp: Ch. 21, 22`

## Launch overhead is a fixed tax
Each kernel launch costs **≈ 3-10 µs** of host-side time and a similar-order latency before the first block starts *(approx.)*. A kernel that does 2 µs of real work is dominated by launching.
Example: a model with 1,000 tiny kernels (each 5 µs of GPU work) launched one by one: if launch is 5 µs and the GPU is idle during gaps ⇒ ≈ 5-10 ms, **half or more of it overhead**. This is why small-batch inference is "launch-bound".

## CUDA graphs
Capture a sequence of operations once (kernels, copies, dependencies) as a **graph**; launch the whole graph with one API call. Per-node launch overhead drops to ≈ 1 µs or less, and the driver can pre-plan dependencies. The 1,000-kernel example drops from ≈ 5-10 ms of overhead to ≈ 1 ms. Restriction: shapes and arguments are fixed at capture (updatable with graph-update APIs).

## Fusion vs graphs
Fusion removes **traffic and launches**; graphs remove **only launch overhead**. Use graphs when you cannot fuse (different shapes/libraries) and fusion when the intermediate traffic matters.

## Dynamic parallelism
A running kernel can launch **child grids** without returning to the host (device-side `<<<>>>`). Natural for recursion/adaptive refinement (quad-trees, adaptive mesh), where the amount of child work depends on the data. Costs: each child launch has overhead comparable to host launches, many tiny children are slower than a flat, data-parallel reformulation, and resources are reserved for pending launches. Use when the structure is truly irregular and the children are large; otherwise prefer flattening (frontier queues as in E10).

## 🎬 VIZ-LAUNCH-OVERHEAD: "Gaps between kernels"
- *Canvas:* a timeline with **Host** and **Device** lanes; N kernels as bars on the device lane with gaps equal to launch overhead.
- *Controls:* **Kernels (1-200)**, **GPU time per kernel**, **Launch overhead**, **Mode** (individual launches / CUDA graph / fused into one).
- *Readouts:* **total time**, **% overhead**, **GPU utilization**.
- *Aha moment:* for 5 µs kernels, "graph" and "fused" collapse the gaps; for 5 ms kernels all three modes are indistinguishable.

## Check yourself
1. Kernel work = 3 µs, launch overhead = 5 µs, 1,000 launches: overhead share of total?
2. Name one situation where dynamic parallelism is justified and one where it is not.
3. Which reduces *memory traffic*: fusion or graphs?

*PMPP reference:* Ch. 21 (CUDA dynamic parallelism: motivation, overhead, nested kernels, memory visibility between parent and child, streams), Ch. 22 (advanced practices: asynchronous execution and graphs context).

---

# NEW CHAPTER F8: Numerical precision and mixed precision
`id: F8 · part: F · est: 35 min · prereqs: E2, E3, F3 · problems: proposed CU-056 · pmpp: Ch. 6, 22 (partial)`

## Why precision is a performance topic
Halving the bytes per element **doubles** memory-bound throughput; tensor cores run 8-16× faster than FP32 cores on lower precision. But fewer mantissa bits mean larger rounding error and a narrower range.

## The formats *(spec)*
| Format | Layout (sign/exp/mantissa) | Unit roundoff u | Max finite | Typical use |
|---|---|---|---|---|
| FP32 | 1 / 8 / 23 | 2⁻²⁴ ≈ 6.0×10⁻⁸ | 3.4×10³⁸ | default compute, accumulators |
| TF32 | 1 / 8 / 10 (19 bits used) | 2⁻¹¹ ≈ 4.9×10⁻⁴ | 3.4×10³⁸ | tensor-core matmul inputs |
| FP16 | 1 / 5 / 10 | 2⁻¹¹ ≈ 4.9×10⁻⁴ | **65,504** | inference, training with loss scaling |
| BF16 | 1 / 8 / 7 | 2⁻⁸ ≈ 3.9×10⁻³ | 3.4×10³⁸ | training (FP32-like range) |
| FP8 E4M3 | 1 / 4 / 3 | 2⁻⁴ = 0.0625 | 448 | inference/training with scaling |
| FP8 E5M2 | 1 / 5 / 2 | 2⁻³ = 0.125 | 57,344 | gradients |
Rule: **range** (exponent bits) decides overflow/underflow; **precision** (mantissa bits) decides rounding error.

## Mixed precision: what to keep in FP32
- **Accumulators.** A dot product of K terms in FP16 accumulating in FP16 has error growing ~K·u; tensor cores accumulate in FP32 (or higher) so error depends on the *input* rounding only.
- **Reductions** across many elements (sums, norms, softmax denominators, losses).
- **Master weights** in training (updates of 10⁻⁵ relative size vanish if added to FP16 weights; u = 4.9×10⁻⁴).
- **Exponentials**: in FP16, e^x overflows for x > 11.09 (e¹² = 162,755 > 65,504), which is another reason softmax subtracts the row max (E3).

## Loss scaling (FP16 training)
Gradients are small; many fall below FP16's smallest normal (≈ 6.1×10⁻⁵) and flush to zero. Multiply the loss by a scale S (e.g., 1,024) before backward, divide gradients by S afterwards; reduce S when overflow occurs. BF16 has FP32's range so it generally needs no scaling.

## Bytes, not just FLOPs
Switching a memory-bound elementwise kernel from FP32 to FP16 halves bytes ⇒ ~2× faster in the time model of A5 (N = 2²⁶ ReLU: 0.31 ms → 0.16 ms on an A100). A matmul switching to FP16 tensor cores moves from the FP32 roof (19.5) to 312 TFLOPS, which pushes the ridge to ≈ 153 FLOP/B (D2).

## Error you can compute
Single FP16 rounding: relative error ≤ u = 4.9×10⁻⁴; product of two FP16 numbers computed exactly then rounded: ≤ u; sum of K FP16 terms accumulated in FP16: worst case ≈ K·u (with K = 1,024 that is ~0.5, so useless), accumulated in FP32: ≈ u + K·6×10⁻⁸ (6×10⁻⁵ for K = 1,024).

## 🎬 VIZ-PRECISION-LADDER: "Same sum, four formats"
- *Canvas:* a number line with the representable values of the chosen format near the current value (spacing visible); a bar for "error".
- *Controls:* **Format**, **Operation** (sum of N ones, dot product, softmax of logits), **Accumulator precision**, **N**.
- *Animation:* the FP32 accumulator stalls at 16,777,216 when adding ones; FP16 stalls at 2,048 (spacing becomes 2 above 2¹¹). Switching the accumulator to a wider type fixes it.
- *Readouts:* **result**, **true value**, **relative error**, **bytes moved**.
- *Aha moment:* FP16 "sum of ones" gives 2,048, **stops 98% early on a 100,000-element sum**.

## Check yourself
1. Why does an FP16 running sum of ones stop at 2,048?
2. At what logit value does FP16 `exp` overflow?
3. Why do mixed-precision matmuls keep FP32 accumulators?

## Proposed problem
**CU-056 Mixed-precision dot product**: FP16 inputs, FP32 accumulator; compare against FP16-only accumulation; report shows bytes saved and max error.

*PMPP reference:* Ch. 6 (numerical considerations: floating-point precision, accuracy and the non-associativity of summation in the performance chapter; reduction order discussion in Ch. 10), Ch. 22 (reduced precision and future evolution). **Not in PMPP's main text:** BF16/TF32/FP8 details, loss scaling: cite vendor docs and the mixed-precision-training literature.

---

# NEW CHAPTER F9: Multi-GPU CUDA programming
`id: F9 · part: F · est: 40 min · prereqs: A2, F2, F4 · problems: CU-047, CU-051 (+ proposed CU-057) · pmpp: Ch. 20, 22`

F4 explained the *collective* (AllReduce) and its cost. This chapter covers the CUDA-level mechanics of using several GPUs: choosing a device, moving data between GPUs, splitting a problem, overlapping communication, and predicting how well it scales.

## Several devices, one host program
`cudaGetDeviceCount(&n)` reports how many GPUs the process can see. Each GPU is a separate device with its own memory, its own streams and events, and its own copy of everything in chapters A-D. Nothing is shared automatically: a pointer from `cudaMalloc` on GPU 0 belongs to GPU 0.

## Current device is thread state
`cudaSetDevice(d)` sets the **current device for the calling host thread**. Every later call on that thread (`cudaMalloc`, stream or event creation, kernel launch) targets that device until you change it. The default is device 0, so a program that forgets `cudaSetDevice` puts all its memory and work on GPU 0.
```cuda
for (int d = 0; d < nGpu; ++d) {
    cudaSetDevice(d);                       // everything below belongs to GPU d
    /* cudaMalloc(&buf[d], ...); cudaStreamCreate(&stream[d]); */
    /* kernel<<<grid, block, 0, stream[d]>>>(buf[d], ...); */   // async, returns at once
}
for (int d = 0; d < nGpu; ++d) { cudaSetDevice(d); cudaDeviceSynchronize(); }
```
Because launches are asynchronous (A2), one host thread can start work on all GPUs and they run concurrently. Rules that catch people:
- A stream or event belongs to the device that was current when it was created. Launching a kernel into another device's stream fails.
- `cudaStreamWaitEvent` **may** wait on an event recorded on another device. This is how you order work across GPUs.

## Topology: who is connected to whom
GPUs in one server are linked by **NVLink** (direct GPU-to-GPU), through an **NVSwitch** (every GPU reaches every other at full speed), or only through **PCIe** (possibly via the CPU, possibly across two CPU sockets).

| Link *(spec / approx.)* | Per-direction bandwidth |
|---|---|
| PCIe 4.0 x16 | ~25-32 GB/s |
| A100 NVLink 3 (12 links) | ~300 GB/s (600 GB/s bidirectional) |
| H100 NVLink 4 | ~450 GB/s (900 GB/s bidirectional) |
| Node-to-node InfiniBand (200 Gbit/s NIC) | ~25 GB/s |

`nvidia-smi topo -m` prints a matrix of how each pair connects: `NV#` (NVLink, # links), `PIX`/`PXB` (PCIe bridges), `PHB` (through the CPU host bridge), `SYS` (across CPU sockets). A copy between two `NV12` GPUs is about **10×** faster than between two `SYS` GPUs. Always check topology before you decide how to split work.

## Peer-to-peer access and copies
Two GPUs can touch each other's memory directly (**peer access**) when the hardware supports it.
- `cudaDeviceCanAccessPeer(&ok, a, b)` asks whether device *a* can access device *b*.
- With device *a* current, `cudaDeviceEnablePeerAccess(b, 0)` lets *a* read and write *b*'s memory. It is **one-directional**; enable both ways if you need both.
- With peer access enabled (and unified virtual addressing), a kernel on *a* may dereference a pointer into *b*'s memory. Each access then travels over the link, so it is as slow as the link and not coalescing-friendly. Prefer copying a block over the link, then computing locally.
- `cudaMemcpyPeerAsync(dst, dstDev, src, srcDev, bytes, stream)` copies GPU to GPU. With P2P it goes straight over NVLink/PCIe; **without it the driver stages through host memory** (two PCIe hops).

Calculation: 1 GB from GPU 0 to GPU 1. Direct over NVLink at 300 GB/s: 1 GB ÷ 300 GB/s ≈ **3.3 ms**. Staged through the host over PCIe 4.0 at 25 GB/s per hop: 40 ms + 40 ms = **80 ms**, about **24× slower**.

## Programming patterns
1. **One thread (or process) drives all GPUs** with the loop above. Simple, good for learning and small node counts.
2. **One process per GPU** (the norm for MPI and NCCL jobs, and for data-parallel training frameworks): each process calls `cudaSetDevice(local_rank)` once, owns one GPU, and exchanges data via NCCL or CUDA-aware MPI. Failures and driver state stay isolated per GPU, and scaling to many nodes uses the same code.
Pin each process to the CPU socket closest to its GPU (NUMA affinity); a GPU reached through the far socket sees lower copy bandwidth (the `SYS` case).

## Domain decomposition and halo exchange
To split a stencil or grid problem, give each GPU a piece of the domain. Neighbouring pieces need each other's border cells (the **halo**, as in E4) every iteration, so GPUs exchange borders.

Take a cube of side *n* per GPU with stencil radius *r*:
$$\text{halo cells} = 6\,r\,n^2,\qquad \text{compute cells} = n^3,\qquad \text{ratio} = \frac{6r}{n}$$
This is the **surface-to-volume ratio**: communication grows with the surface, compute with the volume. Bigger pieces mean relatively less communication.

Worked example: n = 512, r = 1, FP32.
- Halo bytes per exchange: 6 × 512² × 4 B = **6.3 MB**.
- Compute (memory-bound sweep reading and writing every cell): 2 × 512³ × 4 B = 1.07 GB ÷ 1.73 TB/s ≈ **0.62 ms**.
- Exchange over NVLink at 300 GB/s: 6.3 MB ÷ 300 GB/s ≈ **21 µs** (3% of compute). Over PCIe at 25 GB/s: **252 µs** (about 40% of compute).

How you cut the domain matters. A global N³ grid split into **slabs** along one axis gives each GPU halo 2rN² *regardless of p*, while compute per GPU shrinks as N³/p, so the ratio 2rp/N **grows with p**. Splitting in 3D blocks gives a ratio that grows only like p^(1/3).

## Overlapping communication with compute
Reuse the stream ideas of F2:
1. Compute the **boundary layer** first on stream A.
2. Start the halo copies on a communication stream as soon as the boundary is done.
3. Compute the **interior** on stream B at the same time.
4. Order everything with events (`cudaEventRecord`, `cudaStreamWaitEvent`).
The exchange is fully hidden when `T_comm ≤ T_interior`. In the example above, NVLink hides completely; PCIe also hides (252 µs < ~0.6 ms), but only if you actually overlap.

## Scaling: strong, weak, efficiency
- **Strong scaling:** fixed total problem, more GPUs. Speedup S(p) = T₁ / T_p, efficiency E(p) = S(p) / p.
- **Weak scaling:** work per GPU fixed, problem grows with p. Efficiency E_w = T₁ / T_p (ideal 1).
A useful model: `T_p = T_serial + T_par / p + T_comm(p)`.

Worked example: T₁ = 100 ms of parallel work, gradient AllReduce of 5.8 ms (F4 example).
- 8 GPUs, no overlap: T₈ = 12.5 + 5.8 ≈ 18.3 ms ⇒ S = 5.5, **E = 68%**.
- 8 GPUs, communication fully overlapped with backward compute: T₈ ≈ max(12.5, 5.8) = 12.5 ms ⇒ S = 8, E = 100% (ideal case).
Amdahl (A5) still applies: any serial part, including host-side work and launch gaps (F7), caps strong scaling.

## Worked example: matrix multiply on 4 GPUs
Split C = A × B by **rows of A** across p GPUs and replicate B (N = 8,192, FP32, p = 4).
- Compute per GPU: 2 · (N/p) · N² = 275 GFLOP ⇒ ≈ **17.6 ms** at 15.6 TFLOPS (80% of 19.5).
- Communication: broadcast B, N² × 4 B = 268 MB ⇒ ≈ **0.9 ms** at 300 GB/s (≈ 5% of compute).
- As p grows, compute per GPU shrinks like 1/p but each GPU still needs all of B, so efficiency falls. A **2D decomposition** (SUMMA-style) cuts per-GPU communication to about N²/√p words.

## Multi-GPU pitfalls
| Bug | Symptom | Fix |
|---|---|---|
| Forgot `cudaSetDevice` | GPU 0 runs out of memory while others idle | set the device before every allocation and launch on that thread |
| Pointer used on the wrong device | illegal access or wrong data | track which device owns each pointer |
| Peer access not enabled | illegal access, or a copy 10-20× slower than expected | `cudaDeviceCanAccessPeer` + `cudaDeviceEnablePeerAccess`, both directions if needed |
| Stream/event from another device | launch error | create each stream/event while its device is current |
| Mismatched collectives | hang (F4) | all ranks call the same collectives, order and sizes |
| Load imbalance | scaling flattens | split by cost, not by element count |
| Unordered cross-GPU float sums | results differ in last digits | compare with a tolerance (E2) |

## Beyond one node
Across nodes the same ideas hold with a slower link (InfiniBand ~25 GB/s per NIC) and more latency. **CUDA-aware MPI** and **GPUDirect RDMA** let a NIC read GPU memory directly, avoiding a host copy. The hierarchy (NVLink inside a node, network between nodes) is why collective libraries do a local reduce first, then a cross-node step.

## 🎬 VIZ-MULTIGPU-TOPOLOGY: "Who can talk to whom?"
- *Canvas:* GPUs drawn as boxes (4 or 8), links drawn between them with thickness proportional to bandwidth and colour by type (NVLink, PCIe switch, CPU bridge, cross-socket link). Two CPU sockets sit at the top.
- *Controls:* **Topology preset** (8 GPU NVSwitch / 4 GPU NVLink mesh / PCIe tree across 2 sockets), **Source GPU**, **Destination GPU**, **Data size**, **Show topo matrix** toggle.
- *Animation:* picking two GPUs lights the path hop by hop; the slowest hop is outlined as the **bottleneck**; packets stream along the path.
- *Readouts:* **hops**, **bottleneck bandwidth**, **time for D bytes**, and the code `NV12` / `PIX` / `PHB` / `SYS` for that pair; a full pairwise matrix appears when toggled.
- *Aha moment:* on the PCIe-tree preset, GPUs on opposite sockets are 10× slower to reach than neighbours, so "GPU 0 ↔ GPU 7" is not the same cost as "GPU 0 ↔ GPU 1".
- *Accessibility:* "GPU 0 to GPU 5: 3 hops, bottleneck 25 GB/s (SYS). 1 GB takes 40 ms."
- *Data note:* share the topology model with VIZ-RING-ALLREDUCE.

## 🎬 VIZ-P2P-ACCESS: "Direct or via the host?"
- *Canvas:* two GPU boxes with a host box between them; code panel on the left listing `cudaSetDevice`, `cudaDeviceEnablePeerAccess`, and a `cudaMemcpyPeerAsync`.
- *Controls:* checkbox **Peer access enabled (0→1)**, checkbox **Peer access enabled (1→0)**, a **Kernel on GPU 0 reads GPU 1 memory** button, **Copy size**.
- *Animation:* with access off, a copy visibly goes GPU1 → host → GPU0 (two hops, two time bars). With access on, one direct hop. The kernel-read button shows a red "illegal access" chip if access is off, or small packets over the link if on.
- *Readouts:* **copy time**, **hops**, **speed-up of direct vs staged**.
- *Aha moment:* peer access is directional; enabling 0→1 does not allow 1→0.

## 🎬 VIZ-DEVICE-CONTEXT: "Which GPU is current?"
- *Canvas:* a host-thread timeline of API calls; below it, one memory bar per GPU (4 GPUs).
- *Controls:* toggle **Call cudaSetDevice before each allocation**, **Number of buffers**, **Buffer size**, `Stepper`.
- *Animation:* without `cudaSetDevice` every allocation lands on GPU 0 and its bar fills to the top and turns red ("out of memory") while GPUs 1-3 stay empty; with it, bars fill evenly.
- *Aha moment:* "the current device is state on the calling thread", visible as a highlighted GPU that changes only when you call `cudaSetDevice`.

## 🎬 VIZ-HALO-EXCHANGE: "Cut the grid, pay the border"
- *Canvas:* a 2D grid (e.g., 24×24) split among 4 or 8 GPUs, each tile coloured; halo cells drawn as a lighter frame; arrows between neighbouring tiles.
- *Controls:* **Decomposition** (1D slabs / 2D blocks), **GPUs (2-16)**, **Stencil radius r**, **Link** (NVLink / PCIe), **Overlap comm with compute** toggle, `Stepper`.
- *Animation:* each step shows compute (tile fills), halo copy (arrows), and — with overlap on — the interior compute running at the same time as the copy, drawn on a timeline below.
- *Readouts:* **compute cells**, **halo cells**, **surface-to-volume ratio**, **time per iteration**, **comm hidden %**.
- *Aha moment:* raise GPUs with slab decomposition and the ratio climbs; switch to 2D blocks and it climbs more slowly. Toggle overlap and the iteration time drops to max(compute, comm).

## 🎬 VIZ-SCALING-CURVE: "Where does scaling bend?"
- *Canvas:* speedup (y) vs number of GPUs (x, 1-64) with the ideal line dashed; a shaded gap shows the loss; second panel shows efficiency %.
- *Controls:* **Mode** (strong / weak), **Serial fraction** slider, **Comm model** (none / constant AllReduce / ring AllReduce with α-β), **Link**, **Overlap** toggle.
- *Animation:* dragging any control redraws the curve; the point where efficiency drops below 80% is marked.
- *Readouts:* **speedup**, **efficiency**, **comm share of step time** at the selected GPU count.
- *Aha moment:* with constant communication and no overlap, strong scaling flattens early; overlap pushes the bend far to the right.

## Check yourself
1. What does `cudaSetDevice(2)` change, and for which thread?
2. A kernel on GPU 0 dereferences a pointer allocated on GPU 1 and fails. Name two things to check.
3. Cube pieces of side n = 256, radius 1: what fraction of cells is halo?
4. Why does a slab decomposition scale worse than a 3D block decomposition as p grows?
5. When is a halo exchange fully hidden by overlap?

## Pitfalls
- Assuming all GPU pairs have the same bandwidth.
- Measuring multi-GPU time without synchronizing every device.
- Using the default device everywhere and wondering why only GPU 0 is busy.

## Practice
[CU-047 Multi-GPU AllReduce](problem:CU-047) · [CU-051 Bug Hunt: NCCL Deadlock](problem:CU-051)
**Proposed:** CU-057 Multi-GPU halo exchange (1D stencil split over 2-4 simulated GPUs; the report shows halo bytes, link time, and overlap).

*PMPP reference:* Ch. 20 (programming a heterogeneous cluster: domain partitioning, halo exchange, overlapping communication with computation, CUDA-aware MPI), Ch. 22 (advanced practices and multi-GPU context). **Not in PMPP:** NVLink/NVSwitch bandwidth figures and `nvidia-smi topo` notation: cite NVIDIA architecture whitepapers and the CUDA Programming Guide.

---

# APPEND TO F6: Capstone

## The full byte and FLOP ledger for the MLP block (M = 2,048, d = 1,024, h = 4,096, FP32, A100)
Tensor sizes: x = 2,048·1,024·4 = **8.4 MB**; W1 = 1,024·4,096·4 = **16.8 MB**; h = 2,048·4,096·4 = **33.5 MB**; W2 = **16.8 MB**; y = **8.4 MB**.
- FLOPs: first GEMM 2·M·d·h = 17.2 G; second GEMM = 17.2 G; **total 34.4 GFLOP**.
- **Fused-epilogue plan** (2 kernels): GEMM1 reads x + W1 (25.2 MB) and writes h once (33.5 MB) after bias+GELU in registers; GEMM2 reads h (33.5) + W2 (16.8) + residual x (8.4) and writes y (8.4). Total ideal ≈ **126 MB** (+ re-read overhead of tiling).
- **Unfused plan** (5 kernels: GEMM1, bias, GELU, GEMM2, bias+residual): adds read+write of h for bias (67.1 MB) and for GELU (67.1 MB), plus read+write of y for bias (16.8 MB) and residual (read y, x, write y: 25.2 MB) ⇒ **≈ +176 MB**.
- Times (η_m = 0.85, η_c = 0.8): compute **2.2 ms**, fused memory ideal 0.07 ms ⇒ GEMMs are **compute-bound** (AI = 34.4 G ÷ 126 MB ≈ 273 FLOP/B ≫ ridge 9.6, ideal-reuse case). Extra elementwise traffic: 176 MB ÷ 1.73 TB/s ≈ **0.10 ms ≈ 5%** of runtime on CUDA cores. Your report should reproduce these magnitudes and explain the 5% honestly. If your tiled GEMM (T = 16 is memory-bound, see the E7 table) takes far longer than the roughly 0.10 ms of elementwise traffic, the *GEMM* is the bottleneck, not the missing fusion.

## Capstone grading dimensions (suggested)
1. Correct vs NumPy (max error < 1e-4 relative for FP32).
2. Bytes within 1.5× of the ledger above.
3. Zero bank conflicts, zero divergent barriers, zero races.
4. A written bound analysis: which kernels are memory- or compute-bound and why (D2).

## Check yourself (additional)
3. Total FLOPs if d = 2,048 and h = 8,192 with the same M?
4. Why is the fusion benefit only ~5% in this FP32 setting?

*PMPP reference:* Ch. 16 (deep learning: GEMM-based layers, fused operations), Ch. 19 (computational thinking applied to a whole pipeline).

---

# VISUALIZATION GAP-FILL (extra 🎬 specs for the appended blocks)

**Agent:** attach each spec to the end of the named chapter, right after its appended sections. Same visual language, shared primitives, reduced-motion mode and `aria-live` sentence as every other viz. Model functions live in `lib/cuda/model/`.

## 🎬 VIZ-WORK-SPAN: "How parallel is this problem?" (chapter A1)
- *Canvas:* a dependency graph drawn left to right. Nodes are operations; edges are dependencies. Presets: array add (N independent nodes), tree sum (log levels), Fibonacci chain.
- *Controls:* **Preset**, **N**, **Processors p** slider.
- *Animation:* nodes light up level by level; with p processors only p nodes run per step.
- *Readouts:* **work W**, **span S**, **parallelism W/S**, **time on p processors ≥ max(W/p, S)**.
- *Aha moment:* the Fibonacci chain stays at parallelism 1 however large p is.

## 🎬 VIZ-ISSUE-SLOTS: "ILP or more warps?" (chapters A3, B3)
- *Canvas:* four sub-partition scheduler rows over time; each cycle shows which warp issued (coloured), or an empty slot. Below, the pipeline of one FP32 instruction occupying 2 cycles.
- *Controls:* **Warps per scheduler** (1-16), **ILP per thread** (1, 2, 4), **Memory latency**, **Compute instructions between loads**.
- *Readouts:* **issue-slot utilization %**, **warps needed (formula from B3)**.
- *Aha moment:* 4 independent accumulators at 4 warps fill as many slots as 1 accumulator at 16 warps.

## 🎬 VIZ-DIVERGENCE-PROBABILITY: "How often does a warp split?" (chapter C1)
- *Canvas:* a 32-lane strip regenerated randomly; beside it a curve of P(diverge) = 1 − (1−p)³² − p³² against p (log x-axis).
- *Controls:* **p** slider, **Run 1,000 warps**, **Path costs a / b**.
- *Animation:* Monte-Carlo dots fill a histogram of "paths executed per warp" (1 or 2) and converge to the formula.
- *Readouts:* **measured vs formula P(diverge)**, **expected warp time**.
- *Aha moment:* p = 0.01 already splits 27% of warps.

## 🎬 VIZ-BANK-STRIDE-SWEEP (extra mode of VIZ-BANK-GRID, chapter D5)
- *Canvas:* bar chart of conflict degree for strides 1-64.
- *Controls:* **Stride s** slider, **Padding** toggle, **Swizzle (XOR)** toggle.
- *Readouts:* **degree = gcd(s,32)**, **cycles**.
- *Aha moment:* every odd stride is flat at 1; powers of two spike; padding turns stride 32 into stride 33.

## 🎬 VIZ-SHARED-BOUND: "The hidden bottleneck in tiling" (chapter D4)
- *Canvas:* two pipes feeding an FMA block: shared-memory loads (128 B/cycle) and FMA issue (2 warp-FMAs/cycle). Counters show cycles needed for each.
- *Controls:* **Register tile R** (1, 2, 4, 8), **Profile**.
- *Animation:* at R = 1 the load pipe is saturated (4× the FMA time) and the FMA block idles 75%; at R = 4 both pipes are balanced.
- *Readouts:* **loads per warp-FMA = 2/R**, **limiting resource**, **% of FMA peak**.
- *Aha moment:* the bottleneck moves from shared bandwidth to compute at R = 4.

## 🎬 VIZ-FLOAT-ACCUMULATION: "Sum of ones" (chapter E2, shares model with F8)
- *Canvas:* a running total with a number line showing float spacing near the total.
- *Controls:* **Accumulation** (sequential / tree / Kahan), **Format** (FP32 / FP16), **N**.
- *Animation:* sequential FP32 stalls at 16,777,216; FP16 at 2,048; tree keeps counting.
- *Readouts:* **result**, **exact**, **relative error**.

## 🎬 VIZ-SCAN-LOOKBACK: "Single-pass scan" (chapter E6)
- *Canvas:* blocks as columns, each with a status flag (not ready / aggregate / inclusive prefix) and arrows looking back at predecessors.
- *Controls:* **Blocks (4-12)**, **Random scheduling order**, `Stepper`.
- *Animation:* each block publishes its aggregate, then walks back until it finds an inclusive prefix, then publishes its own.
- *Readouts:* **look-back steps per block**, **global words moved: 2N vs 3N-4N for multi-pass**.
- *Aha moment:* waiting only on lower-numbered blocks never deadlocks.

## 🎬 VIZ-RADIX-PASS: "One digit at a time" (chapter E8)
- *Canvas:* an array of 16 keys in binary; a digit-histogram strip; destination arrows.
- *Controls:* **Digit bits r (1, 2, 4)**, **Pass number**, `Stepper`.
- *Animation:* flags → exclusive scan → destinations → scatter; equal digits keep their order (stability highlighted).
- *Readouts:* **passes = ⌈bits/r⌉**, **bytes per pass**.

## 🎬 VIZ-IM2COL: "Convolution as a big matrix" (chapter E4)
- *Canvas:* a small input image, filter window sliding, and the im2col matrix filling one row per window.
- *Controls:* **K (1, 3, 5)**, **Input size**, **C_in**, **Implicit GEMM** toggle.
- *Readouts:* **matrix size**, **memory blow-up (≈ K²×)**, **FLOPs**.
- *Aha moment:* implicit GEMM removes the blown-up buffer.

## 🎬 VIZ-FUSION-BREAKEVEN: "How much does fusion actually save?" (chapters F3, F6)
- *Canvas:* a stacked bar: GEMM time and elementwise-traffic time, with and without fusion.
- *Controls:* **Roof** (FP32 / TF32 / FP16), **Matrix size**, **Fuse** toggle.
- *Readouts:* **elementwise share of runtime** (about 5% on FP32, about 36% on TF32 in the F3 example).
- *Aha moment:* a faster GEMM makes the same fusion matter more.

## 🎬 VIZ-ALPHA-BETA: "Ring or tree?" (chapter F4)
- *Canvas:* time vs message size (log-log) for ring and tree AllReduce, with the crossover marked.
- *Controls:* **GPUs p**, **α**, **β**, **Message size**.
- *Readouts:* **T_ring**, **T_tree**, **winner**.
- *Aha moment:* small messages are latency-bound (tree wins); large messages are bandwidth-bound (ring wins).

## Small extensions to existing viz
- **VIZ-INDEX-CALCULATOR (B1):** add a **"32-bit index"** toggle that wraps the product at 2³¹ for N = 3×10⁹ and shows threads reading the wrong element.
- **VIZ-FLOAT4-BANDWIDTH (D3):** add a **tail panel** showing 250,000 float4 elements plus 3 scalar tail elements for N = 1,000,003.
- **VIZ-ATOMIC-CONTENTION (E5):** add a **warp-aggregated** mode where lanes with the same bin merge into one atomic via `ballot/popc`.
- **VIZ-MAP-FLOW (E1):** show **blocks = capacity C** (SMs × blocks/SM) when grid-stride mode is chosen.
- **VIZ-MEMORY-LADDER (A4):** add a **"copy-kernel benchmark"** button that shows achieved ≈ 80-90% of peak bandwidth.

---

# NEW CHAPTER G1: The calculation workbook
`id: G1 · part: G · est: 90 min · prereqs: A5 and any chapter you are practising · problems: quiz bank (no simulator) · pmpp: Ch. 4-6, 10-11`

**How the agent should use this chapter:** each problem is a card with an input form, a "Check" button that evaluates the formula from `lib/cuda/model/`, and a "Show worked answer" toggle. Inputs are randomizable (seeded) for repeat practice; the answers below are for the fixed seed shown. Profiles: T4 (40 SMs, 64 cores/SM, 320 GB/s, ridge ≈ 25), A100 (108 SMs, 2,039 GB/s, 19.5 TFLOPS, ridge 9.6), H100 (ridge ≈ 20).

## Section 1: Spec-sheet arithmetic
1. T4: 40 SMs × 64 cores, boost 1.59 GHz. Peak FP32? 
2. GDDR6 256-bit bus at 10 Gbit/s per pin. Peak bandwidth?
3. H100: 67 TFLOPS and 3.35 TB/s. Ridge?
4. Copy kernel on an A100 moves 4 GiB in + 4 GiB out in 5.0 ms. Effective bandwidth and η?

## Section 2: Time predictions
5. SAXPY, N = 2²⁷ floats, A100, η_m = 0.85. Predicted time?
6. 2 GB host→T4 copy over PCIe 3.0 at 12 GB/s versus reading 2 GB on-device at 320 GB/s. Ratio?
7. Amdahl: p = 0.9, s = 100. Speedup? What if s → ∞?
8. 10,000 kernel launches of 5 µs overhead each, each doing 3 µs of GPU work: total time and overhead %.

## Section 3: Indexing, warps, occupancy
9. A 20×20 block: warps and lane utilization?
10. A100, 512-thread blocks, 40 regs/thread, no smem: blocks per SM, occupancy, limiter?
11. A100, 256-thread blocks, 80 regs/thread: occupancy? What cap gives 100%?
12. Grid of 2,000 blocks, capacity 864: waves and wave efficiency?
13. N = 10,000,001 with `float4` and block size 256: float4 count, tail elements, blocks.

## Section 4: Memory patterns
14. Stride-4 float loads: sectors per warp and efficiency?
15. `s[4*lane]` on shared memory: conflict degree?
16. Probability that a warp diverges if each lane takes the rare path with p = 0.02.
17. Naive N×N transpose: ratio of actual to ideal bytes?

## Section 5: Algorithms
18. Hillis-Steele vs Blelloch additions for N = 256.
19. Radix sort of 2²⁶ 32-bit keys with 8-bit digits: passes and lower-bound time on A100 (η = 0.85).
20. Histogram: 128 blocks × 1,024 bins: global atomics for merge?
21. Ring AllReduce, D = 400 MB, p = 4, β = 50 GB/s: bytes per GPU and time.
22. Pipelined copy/compute: H = D = 60 ms, K = 20 ms, S = 6. Total time and speedup vs serial.

## Section 6: Roofline and tiling
23. Block tile 64 × 128: AI and bound on A100?
24. Minimum square tile for a compute-bound matmul on the T4 (ridge ≈ 25)?
25. M = N = K = 100, T = 16: tile-load elements (with padding) versus ideal.

## Section 7: Attention, sparse, precision
26. S matrix size for N = 8,192 in FP32?
27. SpMV: nnz = 10⁸ in CSR (12 B/nnz): bytes and minimum time on A100 (η = 0.85). Peak GFLOP/s attainable?
28. conv layer N = 32, C_in = 64, C_out = 128, 56×56, K = 3: FLOPs; im2col buffer size.
29. FP16 sum of ones: where does it stop? FP32?
30. Softmax logit 12 in FP16: does `exp` overflow?

## Section 8: Multi-GPU
31. 3D cube per GPU, n = 512, radius 1, FP32: halo bytes per exchange; time over PCIe (25 GB/s) vs NVLink (300 GB/s).
32. Strong scaling: T₁ = 100 ms, 8 GPUs, constant 5.8 ms communication. Speedup and efficiency without and with perfect overlap.
33. C = A × B, N = 8,192, rows of A split over p = 4 GPUs, B replicated. FLOPs per GPU, compute time at 15.6 TFLOPS, and time to broadcast B at 300 GB/s.
34. Copy 1 GB GPU 0 → GPU 1: direct NVLink (300 GB/s) vs staged via host over PCIe 4.0 (25 GB/s per hop, two hops).

---

# ANSWER KEY (render behind `<details>` toggles)

## Original chapters: "Check yourself"
**A1.** (1) GPU: independent elementwise work... *but* if data starts on the host and is used once, A5's worked example 2 shows PCIe makes the GPU slower than the CPU; the GPU wins only if data stays resident or many passes follow. (2) CPU: span = N (dependency chain). (3) False: each GPU thread is slower; the GPU wins through massive parallelism. *Additional:* (4) W/S = 10⁵. (5) low machine balance: small AI ⇒ memory-bound.
**A2.** (1) No; `cudaDeviceSynchronize` / blocking `cudaMemcpy` / events. (2) Separate address spaces. (3) 2 (in once, out once).
**A3.** (1) GigaThread Engine. (2) No. (3) SFU. *Add.:* (4) 2 cycles. (5) independent instructions in one warp keep the pipe full with fewer warps.
**A4.** (1) Global. (2) Spilled registers / per-thread arrays: physically in global memory. (3) Speed needs proximity and few access ports: small SRAM near the ALUs; large capacity needs distance. *Add.:* (4) L2/L1 hits for a small working set. (5) No: 70% of peak is lower than a typical 80-90%; investigate access pattern/occupancy.
**A5.** (1) 256/8 × 14 = 448 GB/s. (2) min(19.5 T, 2 × 2,039 G) = 4,078 GFLOP/s. (3) because the ratio of times directly says which resource limits runtime.
**B1.** (1) 3,907 blocks. (2) 5·128 + 3 = 643. (3) Out-of-bounds writes may land in padded or unrelated allocations. *Add.:* (4) the index and any byte offset: `size_t`. (5) ⌈33/8⌉ = 5, 5, ⌈33/4⌉ = 9.
**B2.** (1) No ordering or residency guarantee. (2) 8 slots idle (7%). (3) the same program maps to any SM count.
**B3.** (1) 4 warps; 28 lanes wasted. (2) Rows 0 and 1. (3) all state stays resident in the register file. *Add.:* (4) 1 + 400/(3·2) ≈ 68 warps per scheduler: beyond the hardware, so add ILP. (5) 400/416 = 96.2%.
**B4.** (1) Shared memory binds: 164/16 = 10 blocks = 1,280 threads = 62.5%. (2) more blocks fit. (3) high-ILP/register-tiled compute-bound kernels. *Add.:* (4) 40 × 512 = 20,480 regs/block ⇒ 65,536 ÷ 20,480 = 3 blocks = 1,536 threads = **75%**; limiter: registers. (5) 1,000/(2·864) = 57.9%. (6) the register tile lifts AI and cuts shared traffic.
**B5.** (1) Not necessarily: launch is async. (2) leak ⇒ out-of-memory error eventually.
**C1.** (1) No: ≥ 128 aligns on warp boundaries. (2) 7 iterations (the max trip count). (3) the compiler may predicate; behaviour is data-dependent. *Add.:* (4) 47.6%. (5) the warp loops ≈ 7 × 20 = 140 cycles; the average lane needs 3.5 × 20 = 70: 50%.
**C2.** (1) first: RAW (tiles loaded), second: WAR (before overwriting). (2) No. (3) `tile[t] = (idx < n) ? in[idx] : 0; __syncthreads();`
**C3.** (1) orders this thread's own writes for visibility device-wide; does not make others wait. (2) the other block may not be resident. (3) 1,000.
**D1.** (1) 12.5%. (2) the warp walks down a column ⇒ strided. (3) fields interleaved ⇒ strided reads. *Add.:* (4) 12.5%. (5) 4.5×. (6) 50%.
**D2.** (1) 0.167. (2) fewer bytes per FLOP. (3) no. *Add.:* (4) 0.25. (5) T ≥ 100 (T/4 ≥ 25): not a thread-block-sized tile ⇒ register tiling. (6) shrinks the remaining time of compute, leaving memory/elementwise a larger share.
**D3.** (1) misaligned vector access faults. (2) N = 1,000,003 ⇒ 250,000 float4 elements + 3 tail elements. (3) no. *Add.:* (4) ⌈2,500,000/256⌉ = 9,766. (5) already near the ceiling.
**D4.** (1) first: loaded, second: before overwrite. (2) naive 1,024 vs tiled 64. (3) no reuse. *Add.:* (4) 0.5. (5) 7³ × 512 = 175,616. (6) registers/occupancy.
**D5.** (1) 2-way. (2) broadcast. (3) word 4·33 + 7 = 139 ⇒ bank 139 mod 32 = 11. *Add.:* (4) 8-way. (5) gcd(odd, 32) = 1. (6) keeps power-of-two pitch and vector alignment.
**D6.** (1) local (global-backed). (2) constant. (3) enables the read-only path / better scheduling. *Add.:* (4) 65,536/(256×6) = 42 registers. (5) 32 cycles (serialized distinct addresses).
**E1.** (1) no reuse. (2) thread 5: 5, 1,029, … (n = 10,000 ⇒ 10 elements). (3) stateless and deterministic. *Add.:* (4) ≈ 1,214. (5) the mask is regenerated from (seed, i).
**E2.** (1) barriers need all threads. (2) all-negative data ⇒ 0 would win. (3) no: floating-point non-associativity. *Add.:* (4) spacing of floats at 2²⁴ is 2. (5) 2²⁰/512 = 2,048 blocks, 2,048 elements into stage 2. (6) pairwise.
**E3.** (1) the common factor e^{−m} cancels. (2) m = 5, d = 1.149. (3) when |mean| ≫ std. *Add.:* (4) 4C + 4C = 32 KB (16 KB read + 16 KB write). (5) n = 4, μ = 3, M₂ = 2 + 2 + 16·(2·2/4) = 20. (6) no probability matrix is written.
**E4.** (1) 132. (2) uniform broadcast reads. (3) windows don't overlap: no reuse. *Add.:* (4) 2·196·256·256 = 25.7 MFLOP. (5) 1.56. (6) no overlap.
**E5.** (1) read-modify-write race. (2) 16,384. (3) too many bins for shared memory. *Add.:* (4) 131,072. (5) one atomic per group of equal-bin lanes. (6) coalescing.
**E6.** (1) inclusive [3,4,11,11]; exclusive [0,3,4,11]. (2) the exclusive scan of flags = output slot. (3) lanes read positions being written. *Add.:* (4) 16·4 − 15 = 49. (5) flags 1,1,0,1,0,0,1 ⇒ exclusive scan [0,1,2,2,3,3,3] ⇒ out [2,9,4,6]. (6) a block waits only on lower-numbered blocks, which are scheduled first.
**E7.** (1) same address ⇒ broadcast, one transaction. (2) 8. (3) shared memory, occupancy, barriers, edge waste. *Add.:* (4) 64·128/(2·192) = 21.3. (5) 34.4 GB / 1.733 TB/s = 19.8 ms. (6) the ridge moves right.
**E8.** (1) data-independent comparator schedule (0-1 principle). (2) 10. (3) exclusive scan of digit flags gives per-digit destinations. *Add.:* (4) 6·7/2 = 21 stages × 32 = 672. (5) 8. (6) later digit passes must preserve the earlier order.
**E9.** (1) val = [2,1,3], col = [1,0,2], rowptr = [0,1,3,3]. (2) thread-per-row (rows too short for 32 lanes). (3) AI ≈ 0.17.
**E10.** (1) two threads may discover the same vertex. (2) when the frontier is large. (3) the launch boundary is the global barrier.
**F1.** (1) its own value (29 + 4 = 33 > 31). (2) the mask names the participants. (3) warp reduce ⇒ 8 partials in shared ⇒ barrier ⇒ warp 0 reduces. *Add.:* (4) 1. (5) set bits are lanes 2, 4, 5, 7; below lane 5 only lanes 2 and 4 are set ⇒ rank = 2.
**F2.** (1) async DMA needs page-locked pages. (2) 52.5 ms (lower bound 40). *Add.:* (3) h = d = 10, k = 3.33 ⇒ T = 23.3 + 5 × 10 = 73.3 ms (serial: 140 ms). (4) in/out copies serialize.
**F3.** (1) 6 transfers × 4 B = 24 B unfused vs 8 B fused ⇒ 3× less. (2) O(N²) traffic and memory. (3) E3. *Add.:* (4) 268 MB. (5) 4 × 128 × 64 × 4 = 131 KB + 64 KB scores = 196 KB > 164 KB: does **not** fit; use FP16 tiles or B = 64. (6) when the surrounding GEMM dominates (FP32 CUDA cores).
**F4.** (1) volume per GPU → 2D. (2) ranks disagree on collective order/size. (3) AllReduce. *Add.:* (4) 2·(3/4)·400 MB = 600 MB ⇒ 12 ms. (5) per-layer, on the critical path, with activation-sized messages. (6) ReduceScatter + AllGather.
**F5.** (1) race, uninitialized memory/atomic ordering. (2) 12.5% ⇒ D1. *Add.:* (3) D1. (4) first launch includes context/JIT setup.
**F6.** (1) the fused plan avoids at least two full-size round trips of h (bias, GELU). (2) both GEMMs (high AI with reuse); the elementwise parts are memory-bound. *Add.:* (3) 4·2,048·2,048·8,192 = 137.4 GFLOP. (4) CUDA-core GEMM time ≫ elementwise traffic time.
**F7.** (1) 5/(5+3) = 62.5% overhead. (2) justified: adaptive refinement with large children; not: many tiny children. (3) fusion.
**F8.** (1) spacing between FP16 numbers reaches 2 above 2,048, so +1 rounds back. (2) x ≈ 11.09 (e¹² overflows). (3) rounding error grows ~K·u otherwise.
**F9.** (1) the current device for the calling host thread; later allocations, streams, events and launches on that thread target GPU 2. (2) peer access not enabled in that direction (or unsupported by the topology), and the pointer's owning device. (3) 6/256 = **2.3%**. (4) slab halo stays 2rN² while compute per GPU shrinks like 1/p, so the ratio grows with p; 3D blocks grow only like p^(1/3). (5) when T_comm ≤ T_interior (communication fits under the interior compute).

## G1 workbook answers
1. 40·64·2·1.59 = **8.14 TFLOPS**. 2. 256/8·10 = **320 GB/s**. 3. 67/3.35 = **20**. 4. 2·4.295e9 B = 8.59e9 ÷ 5.0e-3 = 1.72 TB/s ⇒ **84%** of 2,039.
5. 12·2²⁷ = 1.61 GB ÷ 1,733 GB/s = **0.93 ms**. 6. 166.7 ms vs 6.25 ms ⇒ **26.7×**. 7. **9.17×**; ceiling **10×**. 8. 10,000 × 8 µs = **80 ms** (if not overlapped), **62.5%** overhead (more if the GPU sits idle; ≈ 50 ms if launches overlap execution).
9. 400 threads ⇒ **13 warps**, 400/416 = **96.2%**. 10. 3 blocks (registers), 1,536 threads, **75%**. 11. 3 blocks ⇒ **37.5%**; ≤ 32 regs for 100%. 12. 3 waves, **77.2%**. 13. 2,500,000 float4, **1 tail**, **9,766** blocks.
14. 16 sectors, **25%**. 15. **4-way**. 16. **47.6%**. 17. **4.5×**.
18. 1,793 vs 510. 19. 4 passes; 4 × 8 B × 2²⁶ = 2.15 GB ÷ 1.733 TB/s ≈ **1.24 ms**. 20. **131,072**. 21. 600 MB per GPU; **12 ms**. 22. 23.3 + 5 × 10 = **73.3 ms**; serial 140 ms ⇒ **1.9×**.
23. 64·128/(2·192) = **21.3 FLOP/B** ⇒ compute-bound (> 9.6). 24. T ≥ 100 (not reachable with thread-per-element tiles). 25. 175,616 vs 125,000: **40% waste**.
26. 8,192² × 4 B = **268 MB**. 27. 10⁸ × 12 B = 1.2 GB ÷ 1.733 TB/s = **0.69 ms**; 2 × 10⁸ FLOP/0.69 ms ≈ **289 GFLOP/s** (bound 340 at peak BW). 28. **14.8 GFLOP**; im2col **231 MB**. 29. FP16 stops at **2,048**; FP32 at **16,777,216**. 30. **Yes** (e¹² = 162,755 > 65,504).
31. 6 × 512² × 4 B = **6.3 MB**; PCIe: **252 µs**; NVLink: **21 µs**. 32. No overlap: 12.5 + 5.8 = 18.3 ms ⇒ S = **5.5**, E = **68%**; perfect overlap: max(12.5, 5.8) = 12.5 ms ⇒ S = **8**, E = **100%**. 33. 2 · 2,048 · 8,192² = **275 GFLOP** ⇒ **17.6 ms**; B = 268 MB ⇒ **0.9 ms** (≈ 5%). 34. Direct **3.3 ms**; staged 40 + 40 = **80 ms**; ratio **≈ 24×**.

---

## Further reading (agent: add as a footer to each affected chapter)
- Hwu, Kirk, El Hajj, *Programming Massively Parallel Processors*, 4th ed. (chapters mapped above).
- Williams, Waterman, Patterson, "Roofline: An Insightful Visual Performance Model" (2009): D2, A5.
- Volkov, "Better Performance at Lower Occupancy" (GTC 2010): B4.
- Harris, "Optimizing Parallel Reduction in CUDA": E2.
- Blelloch, "Prefix Sums and Their Applications"; Merrill & Garland, "Single-pass Parallel Prefix Scan with Decoupled Look-back": E6.
- Milakov & Gimelshein, "Online normalizer calculation for softmax" (2018); Dao et al., "FlashAttention" (2022): E3, F3.
- NVIDIA CUDA C++ Programming Guide and Best Practices Guide; NCCL documentation: D1, D5, F4.
- Bell & Garland, "Implementing Sparse Matrix-Vector Multiplication on Throughput-Oriented Processors" (2009): E9.
- Merrill, Garland, Grimshaw, "Scalable GPU Graph Traversal" (2012): E10.
- Micikevicius et al., "Mixed Precision Training" (2018): F8.
- NVIDIA CUDA C++ Programming Guide, multi-device and peer-to-peer sections; NVIDIA A100/H100 architecture whitepapers (NVLink/NVSwitch): F9.
- Van de Geijn & Watts, "SUMMA: Scalable Universal Matrix Multiplication Algorithm" (1997): F9.
