# Capstone: a fused MLP block

## The goal

Build the forward pass of a transformer-style MLP block on the GPU using kernels you wrote:
```
h = GELU(x · W1 + b1)       (matmul with a fused bias+GELU epilogue)
y = h · W2 + b2 + x         (matmul, bias and residual add)
```
and verify it against the NumPy `Linear` + activation you built in TrenTorch Modules 02 and 03.

## Milestones

1. **Correctness.** Tiled matmul (CU-032) and the activation (CU-008) work individually.
2. **Fusion #1.** Fuse bias + GELU into the first matmul's epilogue (CU-037 pattern).
3. **Fusion #2.** Fuse bias + residual into the second matmul.
4. **Account for bytes.** Use the report to compare your fused block against the unfused sequence; explain the difference with a bytes-moved table.
5. **Roofline.** Place each kernel on the roofline and say which are memory- and compute-bound.

## Bridge to TrenTorch

Module 17 (acceleration) is where the framework chooses a faster backend. The capstone is the proof of concept: the same math as Module 03/02, executed by kernels you wrote and measured.

## Interactive: Your block, end to end

<div class="cuda-viz" data-viz="VIZ-CAPSTONE-PIPELINE" data-title="Your block, end to end" data-spec="VIZ-CAPSTONE-PIPELINE"></div>

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

## Interactive: How much does fusion actually save?

<div class="cuda-viz" data-viz="VIZ-FUSION-BREAKEVEN" data-title="How much does fusion actually save?" data-spec="VIZ-FUSION-BREAKEVEN"></div>

## Check yourself

1. How many global writes of the intermediate `h` does the fused version avoid?
2. Which kernel in this block is more likely compute-bound, and why?
3. Total FLOPs if d = 2,048 and h = 8,192 with the same M?
4. Why is the fusion benefit only ~5% in this FP32 setting?

<details class="answers">
<summary>Show answers</summary>

1. the fused plan avoids at least two full-size round trips of h (bias, GELU).
2. both GEMMs (high AI with reuse); the elementwise parts are memory-bound.
3. 4·2,048·2,048·8,192 = 137.4 GFLOP.
4. CUDA-core GEMM time ≫ elementwise traffic time.

</details>

## Practice

[CU-052 Capstone: Fused MLP Block](problem:CU-052)

*PMPP reference:* Ch. 16 (deep learning: GEMM-based layers, fused operations), Ch. 19 (computational thinking applied to a whole pipeline).
