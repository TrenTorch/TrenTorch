# Map: elementwise kernels

## The simplest pattern

A **map** applies the same function independently to every element: `out[i] = f(in[i])`. Vector add, Hadamard product, every activation function (ReLU, Leaky ReLU, Sigmoid, Tanh, Swish, GELU), and Dropout are maps. In TrenTorch Module 02 you wrote these in NumPy; here one thread owns one element.

## Everything you need is in B1, C1, D1, D2

- Index with the global-index formula; guard with `if (i < n)`.
- Consecutive lanes touch consecutive elements: perfectly coalesced.
- No reuse, so no shared memory.
- Low arithmetic intensity, so **memory-bound**: runtime ≈ bytes ÷ bandwidth.

## Grid-stride loop

Instead of launching one thread per element, launch a fixed grid sized for the GPU and let each thread loop:
```cuda
for (int i = blockIdx.x * blockDim.x + threadIdx.x;
     i < n;
     i += blockDim.x * gridDim.x) { /* ... element i ... */ }
```
One launch configuration then handles any `n`, launch overhead is amortized, and the tail effect (B2) disappears. Consecutive lanes still access consecutive elements on every iteration.

## Activation functions: cost per element

| Function | Notes |
|---|---|
| ReLU, Leaky ReLU | one compare/select; branch-free forms (C1) |
| Sigmoid, Tanh, Swish | one `exp` (or `tanh`) per element; `__expf` is faster and less accurate than `expf` |
| GELU (exact) | uses `erff`; more arithmetic but still memory-bound at large `n` |

The fast intrinsics (`__expf`, `__sinf`) use the SFU and trade a few units in the last place for speed. In a memory-bound map the difference barely shows, so prefer the accurate versions unless the problem says otherwise.

## Randomness in a map (Dropout)

Each thread needs its own random number with no shared state. Use a **counter-based** generator: hash `(seed, element index)` into a pseudo-random value. It is deterministic for a given seed (so tests are reproducible) and needs no memory.

## Interactive: One thread, one element

<div class="cuda-viz" data-viz="VIZ-MAP-FLOW" data-title="One thread, one element" data-spec="VIZ-MAP-FLOW"></div>

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

## Check yourself

1. Why does a map kernel not need shared memory?
2. A grid-stride kernel launches 1,024 threads for n = 10,000. How many elements does thread 5 process?
3. Why is a counter-based RNG a good fit for GPUs?
4. A100, block 256, 8 blocks/SM, N = 2²⁸: elements per thread in a grid-stride launch?
5. Why can the backward pass of Dropout avoid storing the mask?

<details class="answers">
<summary>Show answers</summary>

1. no reuse.
2. thread 5: 5, 1,029, … (n = 10,000 ⇒ 10 elements).
3. stateless and deterministic.
4. ≈ 1,214.
5. the mask is regenerated from (seed, i).

</details>

## Practice

[CU-001](problem:CU-001) · [CU-002](problem:CU-002) · [CU-003 ReLU](problem:CU-003) · [CU-004](problem:CU-004) · [CU-005](problem:CU-005) · [CU-006](problem:CU-006) · [CU-007](problem:CU-007) · [CU-008](problem:CU-008) · [CU-009](problem:CU-009) · [CU-010](problem:CU-010) · [CU-011](problem:CU-011) · [CU-012](problem:CU-012)

*PMPP reference:* Ch. 2 (vector addition, kernel launch), Ch. 6 (coarsening/grid-stride patterns).
