# Kernel fusion and attention

## Why fuse

Every kernel reads its inputs from global memory and writes its outputs back. For memory-bound steps that traffic **is** the cost. Chaining three elementwise kernels moves each intermediate to memory and back; one fused kernel does all three in registers and moves only the final result.

Example: `y = relu(x + bias)` unfused: kernel 1 reads x and bias, writes t (3 transfers of 4 B per element); kernel 2 reads t, writes y (2 transfers) = 20 B per element. Fused: read x, bias, write y = 12 B. About **40% less traffic**, so about 40% less time for a memory-bound step.

A **fused epilogue** applies bias and an activation to a matmul's accumulator while it is still in registers, before writing C once (CU-037).

## Attention, and the matrix you never write

Attention computes `softmax(Q Kᵀ / √d) V`. The score matrix `S = Q Kᵀ` is N × N. For N = 4,096 and 4-byte floats that is 64 MB per head, written, re-read for softmax, written again, and re-read for the `V` product. The **FlashAttention** idea removes that traffic:
- process Q in row blocks; for each, stream over K and V in tiles;
- compute a tile of scores, update a running **online softmax** state (E3) and a running output accumulator;
- never store S to global memory.
This uses everything from earlier chapters: tiling (D4), online softmax (E3), fusion.

## TrenTorch connection

Module 12 builds attention in NumPy; Module 17 (acceleration) is where a GPU backend would plug in. The mini-attention problem is a small version of this fusion.

## Interactive: Count the round trips

<div class="cuda-viz" data-viz="VIZ-FUSION-TRAFFIC" data-title="Count the round trips" data-spec="VIZ-FUSION-TRAFFIC"></div>

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

## Interactive: How much does fusion actually save?

<div class="cuda-viz" data-viz="VIZ-FUSION-BREAKEVEN" data-title="How much does fusion actually save?" data-spec="VIZ-FUSION-BREAKEVEN"></div>

## Check yourself

1. Fused vs unfused traffic for `y = relu(a*x + b)` with three element-wise stages?
2. Why does materializing the N × N score matrix hurt at large N?
3. Which earlier chapter supplies the online-softmax trick?
4. S-matrix size (FP32) for N = 8,192?
5. On-chip bytes for Flash tiles with B_r = B_c = 128, d = 64, FP32? Does it fit in 164 KB?
6. When is fusing a bias + GELU epilogue a < 10% win?

<details class="answers">
<summary>Show answers</summary>

1. 6 transfers × 4 B = 24 B unfused vs 8 B fused ⇒ 3× less.
2. O(N²) traffic and memory.
3. E3.
4. 268 MB.
5. 4 × 128 × 64 × 4 = 131 KB + 64 KB scores = 196 KB > 164 KB: does **not** fit; use FP16 tiles or B = 64.
6. when the surrounding GEMM dominates (FP32 CUDA cores).

</details>

## Practice

[CU-037 Fused MatMul + Bias + ReLU](problem:CU-037) · [CU-038 Fused Softmax](problem:CU-038) · [CU-039 Mini Attention](problem:CU-039)

*PMPP reference:* Ch. 16 (deep learning: fused operations context), Ch. 5-6 (tiling). **Not in PMPP:** FlashAttention itself (Dao et al., 2022) and online softmax (Milakov & Gimelshein, 2018).

## Further reading

- Milakov & Gimelshein, "Online normalizer calculation for softmax" (2018); Dao et al., "FlashAttention" (2022)
