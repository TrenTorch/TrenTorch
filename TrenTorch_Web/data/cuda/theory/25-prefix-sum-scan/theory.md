# Prefix sum (scan)

## Definition

An **inclusive scan** of `[a0, a1, a2, a3]` is `[a0, a0+a1, a0+a1+a2, a0+a1+a2+a3]`. An **exclusive scan** shifts that right and starts with the identity (0). Scan looks serial (each output depends on the previous) but can be done in logarithmic depth.

## Why scan matters

It computes *positions*. Stream compaction ("keep elements that pass a test") uses a scan of 0/1 flags to find each survivor's output slot. Radix sort (E8) is built from scans. Many "irregular" algorithms become regular once you have a scan.

## Hillis-Steele (simple, work-inefficient)

In step *k*, every element adds the value `2^k` positions to its left: log₂ N steps, but about N log₂ N additions. Simple and fast for one block. It needs double buffering (or careful ordering) so threads do not read values already updated in the same step.

## Blelloch (work-efficient)

Two sweeps over a tree:
- **Up-sweep (reduce):** build partial sums up the tree; the root holds the total.
- **Down-sweep:** set the root to 0 (identity), then push prefixes back down.
About 2(N−1) additions: **O(N) work** instead of O(N log N), but 2 log₂ N steps. Shared-memory accesses use power-of-two strides, which creates bank conflicts; padding the index fixes it (D5).

## Beyond one block

Scan each block, write each block's total, scan the block totals, then add each block's offset to its elements (three phases, or two kernels).

## Interactive: Two ways to prefix-sum

<div class="cuda-viz" data-viz="VIZ-SCAN-NETWORK" data-title="Two ways to prefix-sum" data-spec="VIZ-SCAN-NETWORK"></div>

## Work and depth: exact counts

| Algorithm | Depth (steps) | Additions |
|---|---|---|
| Sequential | N−1 | N−1 |
| Hillis-Steele (inclusive) | log₂N | N·log₂N − (N−1) |
| Blelloch (exclusive) | 2·log₂N | 2(N−1) |
| Brent-Kung (inclusive) | 2·log₂N − 1 | 2N − 2 − log₂N |
N = 8: 17 / 14 / 11. N = 256: Hillis-Steele **1,793**, Blelloch **510**. N = 1,024: 9,217 vs 2,046 (4.5×). With *p* processors you cannot exploit the depth win if work is high: work-efficient algorithms win once N ≫ p, which is the usual GPU regime.

## Multi-block scan memory traffic

- **Scan-then-propagate:** pass 1 reads N and writes N (partial scans) plus the block sums; the block sums are scanned; pass 2 reads N and writes N (adding offsets). Total **4N words** moved. A "reduce-then-scan" variant has pass 1 only compute block sums (read N, write ~0) and pass 2 do the scan and offset in one go (read N, write N): **3N words**.
- **Decoupled look-back (single pass):** each block publishes its aggregate and reads predecessors' *inclusive prefixes* with flags; reads N, writes N = **2N words**: about **1.5-2× less traffic**, and the scan reaches the speed of a copy. (Merrill & Garland, 2016: not in PMPP; PMPP covers the hierarchical and single-pass/domino-style variants in Ch. 11.) Forward progress relies on blocks being scheduled in order (a block only waits on lower-numbered blocks), an exception to "never wait for other blocks" that is safe by construction.

## Compaction example

Input `[5, 0, 7, 0, 0, 3]`, predicate `x != 0` ⇒ flags `[1,0,1,0,0,1]`; exclusive scan `[0,1,1,2,2,2]`; survivors write to those positions: `out[0]=5, out[1]=7, out[2]=3`; count = last scan + last flag = 3.

## Bank-conflict-free indexing

`#define OFFSET(i) ((i) + ((i) >> 5))` on every shared-memory index in the up-/down-sweep, with the array sized `N + N/32`.

## Interactive: Single-pass scan

<div class="cuda-viz" data-viz="VIZ-SCAN-LOOKBACK" data-title="Single-pass scan" data-spec="VIZ-SCAN-LOOKBACK"></div>

## Check yourself

1. Inclusive vs exclusive scan of `[3, 1, 7, 0]`.
2. How does a scan of 0/1 flags give output positions for compaction?
3. Why does Hillis-Steele need a second buffer?
4. Hillis-Steele additions for N = 16?
5. Compaction of `[2, 9, 0, 4, 0, 0, 6]` keeping nonzeros: scan and output?
6. Why is decoupled look-back "safe" despite inter-block waiting?

<details class="answers">
<summary>Show answers</summary>

1. inclusive [3,4,11,11]; exclusive [0,3,4,11].
2. the exclusive scan of flags = output slot.
3. lanes read positions being written.
4. 16·4 − 15 = 49.
5. flags 1,1,0,1,0,0,1 ⇒ exclusive scan [0,1,2,2,3,3,3] ⇒ out [2,9,4,6].
6. a block waits only on lower-numbered blocks, which are scheduled first.

</details>

## Practice

[CU-034 Prefix Sum (Scan)](problem:CU-034)

*PMPP reference:* Ch. 11 (Kogge-Stone [≈ Hillis-Steele], Brent-Kung, coarsening, segmented/hierarchical scan, single-pass scan), Ch. 9 (compaction relates to histogram-style output positioning).

## Further reading

- Blelloch, "Prefix Sums and Their Applications"; Merrill & Garland, "Single-pass Parallel Prefix Scan with Decoupled Look-back"
