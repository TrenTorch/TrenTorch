# Warp divergence

## The problem

All 32 lanes of a warp share one instruction stream. What if the code says "if this lane's value is positive do A, otherwise do B" and the lanes disagree? The hardware cannot run A and B at the same time for different lanes. It runs **both paths one after the other**, with the lanes that do not belong to a path **masked off** (they sit idle), then the warp **reconverges** and continues together. That serialization is **warp divergence**.

```
warp:  lanes 0-31 reach  if (x > 0)  A  else  B
pass 1: run A   active mask = lanes where x > 0
pass 2: run B   active mask = lanes where x <= 0
then:   reconverge, all 32 lanes continue
time = time(A) + time(B)        (instead of max)
```

## What diverges and what does not

Divergence only happens **inside a warp**. A branch whose outcome is the same for all 32 lanes costs nothing extra.

| Condition | Diverges? | Why |
|---|---|---|
| `if (blockIdx.x % 2)` | no | all lanes of a block agree |
| `if (threadIdx.x / 32 == 0)` | no | the condition is constant within each warp |
| `if (threadIdx.x < 16)` | **yes** (warp 0) | lanes 0-15 and 16-31 disagree |
| `if (data[i] > 0)` | **depends on data** | random signs split most warps |

Worst cases: a `switch` with 32 different outcomes serializes up to 32 paths. A loop whose trip count differs per lane keeps the whole warp running for the *largest* trip count (lanes that finish early idle).

## Predication: when the compiler removes the branch

For a short conditional, the compiler may not emit a real branch at all. It computes with a per-lane **predicate** or uses a **select** instruction, so every lane executes the same instructions. A source-level `if` therefore *may* diverge, *may* be predicated. You cannot tell from the source alone. This is why we call the branch-free forms a **hazard removal**, not a guaranteed speed-up.

## Branchless vs divergence

For ReLU there are two ways to write the same function:

```cuda
// branchy form: compiler may or may not emit a divergent branch
if (in[i] > 0.0f) out[i] = in[i]; else out[i] = 0.0f;

// branchless form: one max instruction, every lane runs it, nothing to mask
out[i] = fmaxf(in[i], 0.0f);
```
The branchless form removes the question entirely. It also defines how `-0.0` and NaN behave through `fmaxf`'s documented rules, whereas an ad-hoc comparison may not. Other branch-free idioms: the ternary select `x > 0 ? x : 0`, clamping with `fminf/fmaxf`, and arithmetic masks (use with care around NaN and Inf).

Even for a **memory-bound** kernel such as ReLU, the branch-free form is the right idiom: it costs nothing and removes a hazard. (Chapter D2 shows why ReLU is memory-bound.)

## Volta and later: independent thread scheduling

Since Volta, each thread has its own program counter, so lanes can interleave in more ways and the hardware does not *promise* implicit reconvergence at a fixed point. When you need lanes to be in sync (before a warp shuffle, for example) say so explicitly with `__syncwarp()` or the `_sync` intrinsics (chapter F1).

## Interactive: Both roads, one after the other

<div class="cuda-viz" data-viz="VIZ-DIVERGENCE-LANES" data-title="Both roads, one after the other" data-spec="VIZ-DIVERGENCE-LANES"></div>

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

## Interactive: How often does a warp split?

<div class="cuda-viz" data-viz="VIZ-DIVERGENCE-PROBABILITY" data-title="How often does a warp split?" data-spec="VIZ-DIVERGENCE-PROBABILITY"></div>

## Check yourself

1. In a 256-thread block, does `if (threadIdx.x >= 128)` diverge? Which warps?
2. Each lane loops `tid % 8` times. How long does the warp's loop run?
3. Why can you not say "this `if` always diverges"?
4. Probability that a warp diverges when each lane takes a branch with p = 0.02?
5. Trip counts are 0..7 uniformly; the loop body is 20 cycles. What is the warp's loop time versus the *average* lane's useful time?

<details class="answers">
<summary>Show answers</summary>

1. No: ≥ 128 aligns on warp boundaries.
2. 7 iterations (the max trip count).
3. the compiler may predicate; behaviour is data-dependent.
4. 47.6%.
5. the warp loops ≈ 7 × 20 = 140 cycles; the average lane needs 3.5 × 20 = 70: 50%.

</details>

## Pitfalls

- Branching on data when an arithmetic or intrinsic form exists.
- Arranging data so that neighbouring lanes take different paths when a reordering could make whole warps agree.

## Practice

[CU-003 ReLU](problem:CU-003) · [CU-004 Leaky ReLU](problem:CU-004) · [CU-016 Argmax](problem:CU-016) · [CU-044 Bitonic Sort](problem:CU-044)

*PMPP reference:* Ch. 4 (control divergence, its performance impact, loop divergence with variable trip counts), Ch. 6 (strategies for reducing divergence, data rearrangement).
