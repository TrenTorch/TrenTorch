# Shared memory and tiling

## Shared memory is a scratchpad you control

Shared memory sits on the SM, is about as fast as the L1 cache, and is **managed by you**: you decide what to stage into it and when. It exists to **amortize repeated loads**: load a value from slow global memory *once*, then let many threads read it from fast shared memory.

**When not to use it.** A pure map (ReLU, vector add) loads each element exactly once. There is nothing to reuse, so shared memory only adds a copy and a barrier. Use it when data is read more than once.

## The tiling pattern

Take matrix multiply `C = A × B`. In the naive kernel each thread computes one output and reads a row of A and a column of B from global memory; neighbouring threads re-read the same rows and columns. In the tiled kernel a block cooperatively loads one `T × T` tile of A and one of B into shared memory, **synchronizes**, every thread uses the tiles for T multiply-adds, **synchronizes again**, and moves to the next tile along K.

```cuda
__shared__ float As[T][T], Bs[T][T];
float acc = 0.0f;
for (int t = 0; t < numTiles; ++t) {
    /* each thread loads ONE element of an A tile and ONE of a B tile
       (guard against out-of-range) */
    __syncthreads();                 // tiles fully loaded
    /* T multiply-adds from shared memory */
    __syncthreads();                 // everyone done before tiles are overwritten
}
/* write acc to C (guarded) */
```

## What you save

Each element of A and B is loaded from global memory once per tile instead of once per output. Global traffic drops by a factor of **T** (T = 16: 16× fewer loads). Shared memory use is 2·T²·4 bytes: 2 KB for T = 16, 8 KB for T = 32. Bigger tiles save more but consume more shared memory (lowering occupancy, B4) and registers.

## Edge tiles

When the matrix size is not a multiple of T, the last tiles hang over the edge. Load zeros for out-of-range elements and still reach both barriers (C2).

## Interactive: Load once, use many times

<div class="cuda-viz" data-viz="VIZ-TILING-STEPPER" data-title="Load once, use many times" data-spec="VIZ-TILING-STEPPER"></div>

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

## Interactive: The hidden bottleneck in tiling

<div class="cuda-viz" data-viz="VIZ-SHARED-BOUND" data-title="The hidden bottleneck in tiling" data-spec="VIZ-SHARED-BOUND"></div>

## Check yourself

1. Why are there two `__syncthreads()` in the loop?
2. M = N = K = 1024, T = 16. How many global loads of A (and B) per output element, naive vs tiled?
3. Why is shared memory useless for ReLU?
4. How many shared-memory loads per warp-FMA does a 4×4 register tile need?
5. M = N = K = 100, T = 16: how many tile-load elements are fetched in total?
6. Which resource does a bigger tile consume besides shared memory?

<details class="answers">
<summary>Show answers</summary>

1. first: loaded, second: before overwrite.
2. naive 1,024 vs tiled 64.
3. no reuse.
4. 0.5.
5. 7³ × 512 = 175,616.
6. registers/occupancy.

</details>

## Pitfalls

- Missing the second barrier (WAR race).
- Putting a barrier inside a bounds-check `if`.
- Using a tile so large that occupancy collapses.

## Practice

[CU-031 Matrix Multiplication](problem:CU-031) · [CU-032 Tiled Matrix Multiplication](problem:CU-032)

*PMPP reference:* Ch. 5 (tiled matrix multiplication, boundary checks, impact of memory usage on occupancy), Ch. 6 (thread coarsening).
