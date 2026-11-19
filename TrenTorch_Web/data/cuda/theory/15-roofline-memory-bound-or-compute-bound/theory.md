# Roofline: memory-bound or compute-bound

## Arithmetic intensity

**Arithmetic intensity** (AI) = floating-point operations ÷ bytes moved to and from global memory. It tells you whether a kernel is limited by arithmetic or by memory.

- ReLU: 1 compare-select per element, 4 B read + 4 B written = 8 B → **0.125 FLOP/byte**.
- Vector add: 1 FLOP, 12 B → 0.083. SAXPY: 2 FLOPs, 12 B → 0.167.
- Naive matrix multiply: each output needs 2K FLOPs and 2K loaded floats (8K bytes) → 0.25. With tiles of size T it becomes about T/4 (4 at T = 16, 8 at T = 32). Ideal large square matmul: N/6.

## The roofline

Attainable performance = min( peak compute, AI × peak bandwidth ). The point where the two meet is the **ridge point** = peak FLOPs ÷ peak bandwidth.

| GPU *(spec)* | Peak FP32 | Bandwidth | Ridge (FLOP/byte) |
|---|---|---|---|
| T4 | ~8.1 TFLOPS | 320 GB/s | ~25 |
| A100 | ~19.5 TFLOPS | ~2,039 GB/s | ~9.6 |
| H100 SXM | ~67 TFLOPS | ~3,350 GB/s | ~20 |

A kernel with AI below the ridge is **memory-bound**: runtime ≈ bytes ÷ bandwidth, arithmetic is nearly free. Above it, **compute-bound**.

ReLU at 0.125 versus a ridge of roughly 10-25 sits about two orders of magnitude to the left of the ridge. Its arithmetic units idle almost all the time, waiting for DRAM.

## What the classification tells you to do

- **Memory-bound** (maps, norms, softmax): the only levers are fewer bytes moved, coalesced access, enough warps in flight, and wider loads (D3). "Cleverer math" is pointless.
- **Compute-bound** (large matmul, with reuse): raise reuse (tiling, register blocking), keep the arithmetic pipelines full, avoid divergence.

Runtime for a memory-bound map ≈ **bytes ÷ achievable bandwidth**. For ReLU that is 8N ÷ BW.

## Arithmetic intensity as a diagnosis tool

Before optimizing, compute the kernel's AI and place it on the roofline. If you are already at the memory ceiling, no further tuning helps; stop.

## Interactive: Where does my kernel live?

<div class="cuda-viz" data-viz="VIZ-ROOFLINE" data-title="Where does my kernel live?" data-spec="VIZ-ROOFLINE"></div>

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

## Interactive: Roofline Ladder

<div class="cuda-viz" data-viz="VIZ-ROOFLINE" data-mode="roofline-ladder" data-title="Roofline Ladder" data-spec="VIZ-ROOFLINE-LADDER"></div>

## Check yourself

1. Compute AI of `y[i] = a * x[i] + y[i]` (4-byte floats).
2. Why does tiling a matmul raise AI?
3. A kernel is memory-bound. Does a faster `expf` help?
4. AI of a dot product?
5. Required square tile size for compute-bound FP32 matmul on the T4 (ridge ≈ 25)?
6. Why does a faster roof make fusion more valuable?

<details class="answers">
<summary>Show answers</summary>

1. 0.167.
2. fewer bytes per FLOP.
3. no.
4. 0.25.
5. T ≥ 100 (T/4 ≥ 25): not a thread-block-sized tile ⇒ register tiling.
6. shrinks the remaining time of compute, leaving memory/elementwise a larger share.

</details>

## Pitfalls

- Counting only the loads, forgetting the stores.
- Quoting AI with data that actually comes from cache (the roofline uses DRAM bytes).

## Practice

[CU-003 ReLU](problem:CU-003) · [CU-005 Sigmoid](problem:CU-005) · [CU-031 Matrix Multiplication](problem:CU-031)

*PMPP reference:* Ch. 5 (compute-to-global-memory-access ratio; the roofline idea appears in the Ch. 5 discussion of arithmetic intensity), Ch. 6 (performance checklist).

## Further reading

- Williams, Waterman, Patterson, "Roofline: An Insightful Visual Performance Model" (2009)
