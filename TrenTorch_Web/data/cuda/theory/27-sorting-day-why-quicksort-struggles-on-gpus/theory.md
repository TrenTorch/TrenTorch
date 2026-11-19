# Sorting day: why quicksort struggles on GPUs

## Quicksort in one paragraph

Pick a pivot, partition the array into "less than" and "greater than", recurse on both halves. On a CPU, it is excellent. On a GPU it is awkward for three reasons.

1. **Data-dependent branching.** The core step asks `if (a[i] < pivot)` per element. Neighbouring lanes hold random values, so the branch splits warps (C1) and the partition runs at a fraction of full efficiency.
2. **Irregular, shrinking parallelism.** The recursion tree starts with one big partition (little parallelism to exploit at the first few levels) and ends with many tiny ones (too small to fill a warp). Sub-problems have wildly different sizes, so blocks finish at different times (B2 tail effect).
3. **Scatter writes.** Each element goes to a data-dependent position, which tends to break coalescing (D1).

GPU quicksorts exist and can be made to work, but they are rarely the fastest choice. The better answer is to pick an algorithm whose control flow does not depend on the data.

## Bitonic sort: a fixed network

A **sorting network** is a fixed schedule of compare-exchange operations: "compare elements *i* and *j*, put the smaller first". The schedule never looks at the data. Bitonic sort builds one for powers of two:
- Comparators per stage: N/2, all independent.
- Stages: log₂N · (log₂N + 1) / 2, so 55 stages for N = 1,024.
- Total work O(N log² N): more than quicksort's average, but perfectly regular.
Each compare-exchange can be written branch-free with `fminf`/`fmaxf` (or integer min/max), so **there is no divergence at all**.

## Radix sort: built from scan

For each digit (a few bits at a time): compute a flag per element, **scan** the flags to compute each element's destination, then scatter. Work is O(k · N) for k-bit keys, and the passes are stable. Libraries use radix sort for numeric keys because it maps so well onto scan (E6) and coalesced access. It is a great example of the "make irregular work regular with a scan" idea.

## Merge-based sorts

Sort small tiles in shared memory, then merge sorted runs in parallel using binary search to split the work evenly. Useful for comparison sorts of general types.

## Which to choose

| | Divergence | Work | Notes |
|---|---|---|---|
| Naive GPU quicksort | high | ~N log N | irregular, hard to balance |
| Bitonic | none | N log² N | simplest to write, power-of-two N |
| Radix | none | k · N | best for integer/float keys |
| Merge | low | N log N | general comparators |

## Interactive: Partitioning a warp

<div class="cuda-viz" data-viz="VIZ-QUICKSORT-DIVERGENCE" data-title="Partitioning a warp" data-spec="VIZ-QUICKSORT-DIVERGENCE"></div>

## Interactive: A sort that never looks at the data

<div class="cuda-viz" data-viz="VIZ-BITONIC-NETWORK" data-title="A sort that never looks at the data" data-spec="VIZ-BITONIC-NETWORK"></div>

## Counting comparators and bytes

- **Bitonic**, N = 2^k: stages k(k+1)/2, N/2 comparators each ⇒ `N/2 · k(k+1)/2`. N = 1,024 ⇒ 512 × 55 = **28,160** compare-exchanges, vs the information-theoretic ≈ N log₂N = 10,240 (2.75×). N = 2²⁰ ⇒ 20·21/2 = 210 stages × 524,288 = 110 M comparators. With data in shared memory for the first ~log₂(B) stages only the later stages touch global memory.
- **LSD radix sort**, 32-bit keys, *r* bits per pass ⇒ ⌈32/r⌉ passes. r = 8 ⇒ 4 passes; each pass reads and writes the keys once (+ histogram/scan overhead): ≈ 8 B × N per pass. N = 2²⁶ (67 M keys): 4 passes × 537 MB = 2.1 GB ⇒ **≈ 1.2 ms** at 1.73 TB/s *(lower bound; real sorts add scan traffic and reach perhaps 50-70% of that rate)*. Larger *r* ⇒ fewer passes but bigger histograms (2^r bins); 4-8 bits is typical.

## Radix pass step by step

For the current digit: (1) per-block histogram of digit values; (2) exclusive scan over the (digit, block) matrix gives each (block, digit) its global output offset; (3) each element's destination = offset[digit] + its rank among same-digit elements in the block; (4) scatter. Stability (keeping order within equal digits) is what makes successive digit passes compose into a sorted order.

## Merge path (balanced merging)

To merge sorted arrays A and B with *p* workers, find for each worker the split `(i, j)` with `i + j = k·(|A|+|B|)/p` that partitions the merged output evenly: a **co-rank** binary search of O(log N) per worker. Every worker then merges an equal-sized output slice, avoiding the load imbalance of naive partitioning.

## Zero-one principle

A comparator network sorts all inputs iff it sorts all 0/1 inputs. That is the proof behind "the same wiring sorts any input" (check yourself #1 of E8).

## Interactive: One digit at a time

<div class="cuda-viz" data-viz="VIZ-RADIX-PASS" data-title="One digit at a time" data-spec="VIZ-RADIX-PASS"></div>

## Check yourself

1. Why can the same sorting network sort any input?
2. How many stages does bitonic sort need for N = 16?
3. How does a scan of flags give the destination slots in a radix-sort pass?
4. Compare-exchange count of bitonic sort for N = 64?
5. Radix passes for 64-bit keys with 8-bit digits?
6. Why must a radix pass be stable?

<details class="answers">
<summary>Show answers</summary>

1. data-independent comparator schedule (0-1 principle).
2. 10.
3. exclusive scan of digit flags gives per-digit destinations.
4. 6·7/2 = 21 stages × 32 = 672.
5. 8.
6. later digit passes must preserve the earlier order.

</details>

## Practice

[CU-044 Bitonic Sort](problem:CU-044) · [CU-045 Radix Sort](problem:CU-045)

*PMPP reference:* Ch. 12 (merge: co-rank function, parallel merge, tiled merge), Ch. 13 (sorting: radix sort, parallel radix, coalescing optimizations, merge sort), Ch. 11 (scan used inside radix sort).
