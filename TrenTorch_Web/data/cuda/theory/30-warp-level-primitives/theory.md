# Warp-level primitives

## Lanes can talk to each other directly

Within a warp, lanes can exchange register values **without shared memory and without a barrier**. These **warp shuffle** intrinsics take a mask of participating lanes (use `0xffffffff` for the full warp) and a value:
- `__shfl_down_sync(mask, v, delta)`: lane *i* gets lane *i+delta*'s value.
- `__shfl_xor_sync(mask, v, laneMask)`: butterfly exchange.
- `__shfl_sync(mask, v, srcLane)`: broadcast from one lane.
Voting: `__ballot_sync` returns a 32-bit mask of lanes where a predicate holds; `__any_sync`, `__all_sync`. `__syncwarp()` makes lanes reconverge.

## Warp reduction

```cuda
for (int off = 16; off > 0; off >>= 1)
    v += __shfl_down_sync(0xffffffff, v, off);
// lane 0 now holds the sum of all 32 lanes
```
Five steps, no shared memory, no barrier. A full block reduction then needs only one value per warp in shared memory.

## Why the `_sync` and the mask

Since independent thread scheduling (C1) lanes may not be converged. The mask names exactly which lanes must participate, and the call waits for them. Calling a shuffle with a lane missing from the mask but present in the warp is a bug.

## Interactive: Lanes passing notes

<div class="cuda-viz" data-viz="VIZ-SHUFFLE-NETWORK" data-title="Lanes passing notes" data-spec="VIZ-SHUFFLE-NETWORK"></div>

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

## Check yourself

1. What does lane 29 receive from `__shfl_down_sync(mask, v, 4)`?
2. Why is a full-warp mask required if all 32 lanes execute the call?
3. How would you reduce a 256-thread block using shuffles?
4. Barriers per block for a shuffle-based reduction of 256 threads?
5. Given `ballot = 0b1011_0100` and lane = 5, what is `rank`?

<details class="answers">
<summary>Show answers</summary>

1. its own value (29 + 4 = 33 > 31).
2. the mask names the participants.
3. warp reduce ⇒ 8 partials in shared ⇒ barrier ⇒ warp 0 reduces.
4. 1.
5. set bits are lanes 2, 4, 5, 7; below lane 5 only lanes 2 and 4 are set ⇒ rank = 2.

</details>

## Practice

[CU-046 Warp-Shuffle Reduction](problem:CU-046)

*PMPP reference:* Ch. 10 (reduction hierarchy; warp-level shuffle variants appear in later editions' optimizations and in Ch. 22 "advanced practices"), Ch. 9 (aggregation).
