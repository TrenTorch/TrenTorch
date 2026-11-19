# Reduction

## The problem

A **reduction** turns many values into one: sum, max, min, dot product, norm, mean. It is the backbone of layer norm, softmax, losses and attention. It cannot be a pure map because every output depends on all inputs. The trick is a **tree**: add pairs, then add the pair-sums, and so on. N values take $\lceil \log_2 N \rceil$ steps and N−1 additions in total.

## One block's tree

Each thread loads an element into shared memory, then the block halves the active range repeatedly:
```cuda
for (int s = blockDim.x / 2; s > 0; s >>= 1) {
    if (tid < s) sdata[tid] += sdata[tid + s];   // combine two partials
    __syncthreads();                              // finish this level before the next
}
```
After the loop, `sdata[0]` is the block's partial result. To combine blocks you need a second stage: either write one partial per block and launch a second kernel, or have thread 0 of each block do an `atomicAdd` into one global value.

## The optimization ladder

| Step | Idea | What it fixes |
|---|---|---|
| 1 | Interleaved addressing, `if (tid % (2*s) == 0)` | (baseline) divergent, many idle lanes |
| 2 | Strided index, `index = 2*s*tid` | removes divergence but causes shared-memory bank conflicts |
| 3 | **Sequential addressing** (the loop above) | no divergence within warps while `s ≥ 32`, no bank conflicts |
| 4 | **First add during load**: each thread loads two elements and adds them | halves idle threads in the first step |
| 5 | **Warp shuffle** for the last 32 elements (F1) | no shared memory and no barriers for the last 5 levels |
| 6 | **Grid-stride** accumulation per thread before the tree, then atomics or two-pass | handles any N with a modest grid |

## Floating-point is not associative

Different summation orders give slightly different float results. Compare with a **tolerance**, not exact equality, and expect GPU sums to differ in the last digits from a CPU loop.

## Identity elements

Pad out-of-range threads with the operation's identity: 0 for sum, −∞ for max, +∞ for min. Every thread must still reach the barriers (C2).

## Reductions with a payload

**Argmax** reduces (value, index) pairs; define a tie-breaking rule (for example, lowest index) so the result is deterministic. **Dot product** is a map (multiply) fused with a sum. **Mean/variance** use two sums or Welford's update (E3).

## Interactive: Fold the array in half

<div class="cuda-viz" data-viz="VIZ-REDUCTION-TREE" data-title="Fold the array in half" data-spec="VIZ-REDUCTION-TREE"></div>

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

## Interactive: Sum of ones

<div class="cuda-viz" data-viz="VIZ-FLOAT-ACCUMULATION" data-title="Sum of ones" data-spec="VIZ-FLOAT-ACCUMULATION"></div>

## Check yourself

1. Why must every thread, even out-of-range ones, reach each `__syncthreads()`?
2. Why is `0` the wrong padding value for a max reduction over negative numbers?
3. Two correct reductions of the same data differ by 1e-7. Is one a bug?
4. Why does the ones-sum stall at exactly 2²⁴?
5. N = 2²⁰, 256 threads, 2 elements per thread: blocks in stage 1? Elements entering stage 2?
6. Which scheme has the smaller worst-case error bound, sequential or pairwise?

<details class="answers">
<summary>Show answers</summary>

1. barriers need all threads.
2. all-negative data ⇒ 0 would win.
3. no: floating-point non-associativity.
4. spacing of floats at 2²⁴ is 2.
5. 2²⁰/512 = 2,048 blocks, 2,048 elements into stage 2.
6. pairwise.

</details>

## Pitfalls

- `atomicMax` on floats is not built in for all targets; plan a workaround.
- Using the reduction result in the same kernel before all blocks have finished (blocks cannot wait for each other).

## Practice

[CU-013 Sum](problem:CU-013) · [CU-014 Max](problem:CU-014) · [CU-015 Min](problem:CU-015) · [CU-016 Argmax](problem:CU-016) · [CU-017 Dot Product](problem:CU-017) · [CU-018 Mean and Variance](problem:CU-018) · [CU-019 L1 Norm](problem:CU-019) · [CU-020 L2 Norm](problem:CU-020) · [CU-021 Cosine Similarity](problem:CU-021)

*PMPP reference:* Ch. 10 (reduction trees, minimizing divergence, memory divergence, hierarchical reduction, thread coarsening).

## Further reading

- Harris, "Optimizing Parallel Reduction in CUDA"
