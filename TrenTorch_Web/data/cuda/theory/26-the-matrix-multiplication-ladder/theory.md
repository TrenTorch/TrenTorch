# The matrix multiplication ladder

## Why matmul

Linear layers, attention and convolutions (via im2col) all reduce to matrix multiplication. TrenTorch's `Linear` (Module 03) is a matmul plus bias. It is the best example of a kernel you can make dramatically faster by climbing a ladder of ideas, each fixing a measured bottleneck.

## Step by step

| Version | Idea | Global loads per output (K inner dim) | Notes |
|---|---|---|---|
| v1 Naive | one thread per output | 2K | AI ≈ 0.25 FLOP/byte (cache may help) |
| v2 Coalescing fix | map `threadIdx.x` to the **column** axis | 2K | same loads, far better transactions: threads in a warp read consecutive B elements and broadcast one A element |
| v3 Shared-memory tiles | tile size T | 2K / T | AI ≈ T/4; two barriers per tile |
| v4 Thread coarsening | each thread computes several outputs | lower still | more reuse from registers; fewer, fatter threads |
| v5 Vectorized loads | `float4` into shared memory | same | fewer load instructions (D3) |
| v6 Register tiling + padding | each thread holds a small 2D block of C in registers; pad shared tiles | much lower | bank-conflict-free, high AI, register pressure matters |
| v7 Double buffering *(concept)* | load the next tile while computing the current | same | hides load latency; asynchronous copy instructions on newer GPUs; **not simulated here** |

Tensor cores can deliver far more throughput still; they are out of scope for the simulator but you should know they exist.

## Reading the ladder on the roofline

Each version moves the kernel's point up and to the right (D2): fewer bytes per FLOP means higher AI, until you approach the compute roof or run into register/occupancy limits (B4). A well-optimized version reaches a large fraction of peak; do not expect to match a vendor library without tensor cores.

## What each rung costs

Tiling costs shared memory and barriers; coarsening costs registers; vectorizing costs alignment constraints; padding costs a little shared memory. The skill is knowing which bottleneck the *report* shows and choosing the matching rung.

## Interactive: Climb the ladder

<div class="cuda-viz" data-viz="VIZ-MATMUL-LADDER" data-title="Climb the ladder" data-spec="VIZ-MATMUL-LADDER"></div>

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

## Check yourself

1. In v1, why do the 32 lanes of a warp reading `A[row][k]` not cost 32 loads?
2. What is the AI of tiled matmul with T = 32?
3. Name one downside of increasing the tile size.
4. AI of a 64 × 128 block tile?
5. Memory time (η = 0.85) of v3 with T = 16 at N = 4096 on A100?
6. Why does a faster compute roof make bandwidth-optimization matter more?

<details class="answers">
<summary>Show answers</summary>

1. same address ⇒ broadcast, one transaction.
2. 8.
3. shared memory, occupancy, barriers, edge waste.
4. 64·128/(2·192) = 21.3.
5. 34.4 GB / 1.733 TB/s = 19.8 ms.
6. the ridge moves right.

</details>

## Practice

[CU-031](problem:CU-031) · [CU-032](problem:CU-032) · [CU-035 Coarsened](problem:CU-035) · [CU-036 Vectorized + bank-free](problem:CU-036) · [CU-037 Fused MatMul+Bias+ReLU](problem:CU-037)

*PMPP reference:* Ch. 5 (tiled GEMM, the core derivation), Ch. 6 (corner turning, thread coarsening), Ch. 16 (GEMM in deep learning); register tiling and software pipelining are discussed across Ch. 6 and 22. *Tensor cores: not in PMPP's main text; cite vendor architecture whitepapers.*
