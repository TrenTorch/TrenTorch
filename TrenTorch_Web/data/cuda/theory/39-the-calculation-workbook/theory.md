# The calculation workbook

Work each problem with a pen first, then press **Check** to compare your number with the model. Answers are behind a toggle.

Profiles: T4 (40 SMs, 64 cores/SM, 320 GB/s, ridge ≈ 25), A100 (108 SMs, 2,039 GB/s, 19.5 TFLOPS, ridge 9.6), H100 (ridge ≈ 20).

## Section 1: Spec-sheet arithmetic

<div class="g1-card" data-problem="1">

**Problem 1.** T4: 40 SMs × 64 cores, boost 1.59 GHz. Peak FP32? 

<div class="g1-check" data-problem="1"></div>

<details class="answers">
<summary>Show worked answer</summary>

40·64·2·1.59 = **8.14 TFLOPS**.

</details>

</div>

<div class="g1-card" data-problem="2">

**Problem 2.** GDDR6 256-bit bus at 10 Gbit/s per pin. Peak bandwidth?

<div class="g1-check" data-problem="2"></div>

<details class="answers">
<summary>Show worked answer</summary>

256/8·10 = **320 GB/s**.

</details>

</div>

<div class="g1-card" data-problem="3">

**Problem 3.** H100: 67 TFLOPS and 3.35 TB/s. Ridge?

<div class="g1-check" data-problem="3"></div>

<details class="answers">
<summary>Show worked answer</summary>

67/3.35 = **20**.

</details>

</div>

<div class="g1-card" data-problem="4">

**Problem 4.** Copy kernel on an A100 moves 4 GiB in + 4 GiB out in 5.0 ms. Effective bandwidth and η?

<div class="g1-check" data-problem="4"></div>

<details class="answers">
<summary>Show worked answer</summary>

2·4.295e9 B = 8.59e9 ÷ 5.0e-3 = 1.72 TB/s ⇒ **84%** of 2,039.

</details>

</div>

## Section 2: Time predictions

<div class="g1-card" data-problem="5">

**Problem 5.** SAXPY, N = 2²⁷ floats, A100, η_m = 0.85. Predicted time?

<div class="g1-check" data-problem="5"></div>

<details class="answers">
<summary>Show worked answer</summary>

12·2²⁷ = 1.61 GB ÷ 1,733 GB/s = **0.93 ms**.

</details>

</div>

<div class="g1-card" data-problem="6">

**Problem 6.** 2 GB host→T4 copy over PCIe 3.0 at 12 GB/s versus reading 2 GB on-device at 320 GB/s. Ratio?

<div class="g1-check" data-problem="6"></div>

<details class="answers">
<summary>Show worked answer</summary>

166.7 ms vs 6.25 ms ⇒ **26.7×**.

</details>

</div>

<div class="g1-card" data-problem="7">

**Problem 7.** Amdahl: p = 0.9, s = 100. Speedup? What if s → ∞?

<div class="g1-check" data-problem="7"></div>

<details class="answers">
<summary>Show worked answer</summary>

**9.17×**; ceiling **10×**.

</details>

</div>

<div class="g1-card" data-problem="8">

**Problem 8.** 10,000 kernel launches of 5 µs overhead each, each doing 3 µs of GPU work: total time and overhead %.

<div class="g1-check" data-problem="8"></div>

<details class="answers">
<summary>Show worked answer</summary>

10,000 × 8 µs = **80 ms** (if not overlapped), **62.5%** overhead (more if the GPU sits idle; ≈ 50 ms if launches overlap execution).

</details>

</div>

## Section 3: Indexing, warps, occupancy

<div class="g1-card" data-problem="9">

**Problem 9.** A 20×20 block: warps and lane utilization?

<div class="g1-check" data-problem="9"></div>

<details class="answers">
<summary>Show worked answer</summary>

400 threads ⇒ **13 warps**, 400/416 = **96.2%**.

</details>

</div>

<div class="g1-card" data-problem="10">

**Problem 10.** A100, 512-thread blocks, 40 regs/thread, no smem: blocks per SM, occupancy, limiter?

<div class="g1-check" data-problem="10"></div>

<details class="answers">
<summary>Show worked answer</summary>

3 blocks (registers), 1,536 threads, **75%**.

</details>

</div>

<div class="g1-card" data-problem="11">

**Problem 11.** A100, 256-thread blocks, 80 regs/thread: occupancy? What cap gives 100%?

<div class="g1-check" data-problem="11"></div>

<details class="answers">
<summary>Show worked answer</summary>

3 blocks ⇒ **37.5%**; ≤ 32 regs for 100%.

</details>

</div>

<div class="g1-card" data-problem="12">

**Problem 12.** Grid of 2,000 blocks, capacity 864: waves and wave efficiency?

<div class="g1-check" data-problem="12"></div>

<details class="answers">
<summary>Show worked answer</summary>

3 waves, **77.2%**.

</details>

</div>

<div class="g1-card" data-problem="13">

**Problem 13.** N = 10,000,001 with `float4` and block size 256: float4 count, tail elements, blocks.

<div class="g1-check" data-problem="13"></div>

<details class="answers">
<summary>Show worked answer</summary>

2,500,000 float4, **1 tail**, **9,766** blocks.

</details>

</div>

## Section 4: Memory patterns

<div class="g1-card" data-problem="14">

**Problem 14.** Stride-4 float loads: sectors per warp and efficiency?

<div class="g1-check" data-problem="14"></div>

<details class="answers">
<summary>Show worked answer</summary>

16 sectors, **25%**.

</details>

</div>

<div class="g1-card" data-problem="15">

**Problem 15.** `s[4*lane]` on shared memory: conflict degree?

<div class="g1-check" data-problem="15"></div>

<details class="answers">
<summary>Show worked answer</summary>

**4-way**.

</details>

</div>

<div class="g1-card" data-problem="16">

**Problem 16.** Probability that a warp diverges if each lane takes the rare path with p = 0.02.

<div class="g1-check" data-problem="16"></div>

<details class="answers">
<summary>Show worked answer</summary>

**47.6%**.

</details>

</div>

<div class="g1-card" data-problem="17">

**Problem 17.** Naive N×N transpose: ratio of actual to ideal bytes?

<div class="g1-check" data-problem="17"></div>

<details class="answers">
<summary>Show worked answer</summary>

**4.5×**.

</details>

</div>

## Section 5: Algorithms

<div class="g1-card" data-problem="18">

**Problem 18.** Hillis-Steele vs Blelloch additions for N = 256.

<div class="g1-check" data-problem="18"></div>

<details class="answers">
<summary>Show worked answer</summary>

1,793 vs 510.

</details>

</div>

<div class="g1-card" data-problem="19">

**Problem 19.** Radix sort of 2²⁶ 32-bit keys with 8-bit digits: passes and lower-bound time on A100 (η = 0.85).

<div class="g1-check" data-problem="19"></div>

<details class="answers">
<summary>Show worked answer</summary>

4 passes; 4 × 8 B × 2²⁶ = 2.15 GB ÷ 1.733 TB/s ≈ **1.24 ms**.

</details>

</div>

<div class="g1-card" data-problem="20">

**Problem 20.** Histogram: 128 blocks × 1,024 bins: global atomics for merge?

<div class="g1-check" data-problem="20"></div>

<details class="answers">
<summary>Show worked answer</summary>

**131,072**.

</details>

</div>

<div class="g1-card" data-problem="21">

**Problem 21.** Ring AllReduce, D = 400 MB, p = 4, β = 50 GB/s: bytes per GPU and time.

<div class="g1-check" data-problem="21"></div>

<details class="answers">
<summary>Show worked answer</summary>

600 MB per GPU; **12 ms**.

</details>

</div>

<div class="g1-card" data-problem="22">

**Problem 22.** Pipelined copy/compute: H = D = 60 ms, K = 20 ms, S = 6. Total time and speedup vs serial.

<div class="g1-check" data-problem="22"></div>

<details class="answers">
<summary>Show worked answer</summary>

23.3 + 5 × 10 = **73.3 ms**; serial 140 ms ⇒ **1.9×**.

</details>

</div>

## Section 6: Roofline and tiling

<div class="g1-card" data-problem="23">

**Problem 23.** Block tile 64 × 128: AI and bound on A100?

<div class="g1-check" data-problem="23"></div>

<details class="answers">
<summary>Show worked answer</summary>

64·128/(2·192) = **21.3 FLOP/B** ⇒ compute-bound (> 9.6).

</details>

</div>

<div class="g1-card" data-problem="24">

**Problem 24.** Minimum square tile for a compute-bound matmul on the T4 (ridge ≈ 25)?

<div class="g1-check" data-problem="24"></div>

<details class="answers">
<summary>Show worked answer</summary>

T ≥ 100 (not reachable with thread-per-element tiles).

</details>

</div>

<div class="g1-card" data-problem="25">

**Problem 25.** M = N = K = 100, T = 16: tile-load elements (with padding) versus ideal.

<div class="g1-check" data-problem="25"></div>

<details class="answers">
<summary>Show worked answer</summary>

175,616 vs 125,000: **40% waste**.

</details>

</div>

## Section 7: Attention, sparse, precision

<div class="g1-card" data-problem="26">

**Problem 26.** S matrix size for N = 8,192 in FP32?

<div class="g1-check" data-problem="26"></div>

<details class="answers">
<summary>Show worked answer</summary>

8,192² × 4 B = **268 MB**.

</details>

</div>

<div class="g1-card" data-problem="27">

**Problem 27.** SpMV: nnz = 10⁸ in CSR (12 B/nnz): bytes and minimum time on A100 (η = 0.85). Peak GFLOP/s attainable?

<div class="g1-check" data-problem="27"></div>

<details class="answers">
<summary>Show worked answer</summary>

10⁸ × 12 B = 1.2 GB ÷ 1.733 TB/s = **0.69 ms**; 2 × 10⁸ FLOP/0.69 ms ≈ **289 GFLOP/s** (bound 340 at peak BW).

</details>

</div>

<div class="g1-card" data-problem="28">

**Problem 28.** conv layer N = 32, C_in = 64, C_out = 128, 56×56, K = 3: FLOPs; im2col buffer size.

<div class="g1-check" data-problem="28"></div>

<details class="answers">
<summary>Show worked answer</summary>

**14.8 GFLOP**; im2col **231 MB**.

</details>

</div>

<div class="g1-card" data-problem="29">

**Problem 29.** FP16 sum of ones: where does it stop? FP32?

<div class="g1-check" data-problem="29"></div>

<details class="answers">
<summary>Show worked answer</summary>

FP16 stops at **2,048**; FP32 at **16,777,216**.

</details>

</div>

<div class="g1-card" data-problem="30">

**Problem 30.** Softmax logit 12 in FP16: does `exp` overflow?

<div class="g1-check" data-problem="30"></div>

<details class="answers">
<summary>Show worked answer</summary>

**Yes** (e¹² = 162,755 > 65,504).

</details>

</div>

## Section 8: Multi-GPU

<div class="g1-card" data-problem="31">

**Problem 31.** 3D cube per GPU, n = 512, radius 1, FP32: halo bytes per exchange; time over PCIe (25 GB/s) vs NVLink (300 GB/s).

<div class="g1-check" data-problem="31"></div>

<details class="answers">
<summary>Show worked answer</summary>

6 × 512² × 4 B = **6.3 MB**; PCIe: **252 µs**; NVLink: **21 µs**.

</details>

</div>

<div class="g1-card" data-problem="32">

**Problem 32.** Strong scaling: T₁ = 100 ms, 8 GPUs, constant 5.8 ms communication. Speedup and efficiency without and with perfect overlap.

<div class="g1-check" data-problem="32"></div>

<details class="answers">
<summary>Show worked answer</summary>

No overlap: 12.5 + 5.8 = 18.3 ms ⇒ S = **5.5**, E = **68%**; perfect overlap: max(12.5, 5.8) = 12.5 ms ⇒ S = **8**, E = **100%**.

</details>

</div>

<div class="g1-card" data-problem="33">

**Problem 33.** C = A × B, N = 8,192, rows of A split over p = 4 GPUs, B replicated. FLOPs per GPU, compute time at 15.6 TFLOPS, and time to broadcast B at 300 GB/s.

<div class="g1-check" data-problem="33"></div>

<details class="answers">
<summary>Show worked answer</summary>

2 · 2,048 · 8,192² = **275 GFLOP** ⇒ **17.6 ms**; B = 268 MB ⇒ **0.9 ms** (≈ 5%).

</details>

</div>

<div class="g1-card" data-problem="34">

**Problem 34.** Copy 1 GB GPU 0 → GPU 1: direct NVLink (300 GB/s) vs staged via host over PCIe 4.0 (25 GB/s per hop, two hops).

<div class="g1-check" data-problem="34"></div>

<details class="answers">
<summary>Show worked answer</summary>

Direct **3.3 ms**; staged 40 + 40 = **80 ms**; ratio **≈ 24×**.  ---

</details>

</div>
