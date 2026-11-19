# Histogram and atomics

## The write-conflict problem

A histogram counts how many inputs fall in each bin. Many threads may increment the same bin at the same time. A plain `bins[b]++` is a read-modify-write: two threads can read the same old value and both write old+1, losing a count. An **atomic** (`atomicAdd`) performs the whole read-modify-write indivisibly, so the result is correct.

## Contention

Atomics on the same address serialize. If most inputs land in a few bins (skewed data), thousands of threads queue on those few addresses and the kernel crawls even though it is "correct".

## Privatization

Give each block its **own private histogram in shared memory**. Threads do atomics into shared memory (fast, contention limited to one block), then after a barrier the block merges its private copy into the global histogram with one atomic per bin. Global contention drops from (number of elements) to (number of blocks × number of bins).

```cuda
__shared__ unsigned int local[BINS];
/* zero local[] cooperatively; __syncthreads(); */
/* each thread: atomicAdd(&local[bin(x)], 1u) for its elements */
/* __syncthreads(); then merge local[] into global bins with atomicAdd */
```

## Coarsening and the bin count

Letting each thread process several elements reduces the number of threads and the merge overhead. Privatization needs the bin array to fit in shared memory; for huge bin counts, other strategies apply.

## Interactive: Everyone wants the same bin

<div class="cuda-viz" data-viz="VIZ-ATOMIC-CONTENTION" data-title="Everyone wants the same bin" data-spec="VIZ-ATOMIC-CONTENTION"></div>

## Counting atomics precisely

- **Naive global:** one global atomic per input element: N operations (N = 2²⁴ ⇒ 16.8 M).
- **Privatized, per-block histogram:** per block, `elements_per_block` shared atomics plus up to `bins` global atomics for the merge. Global atomics = `blocks × bins`. 128 blocks × 1,024 bins = **131,072** (128× fewer than naive for N = 2²⁴).
- **Capacity limit:** bins × 4 B ≤ shared per block: 164 KB → ≈ 41,000 bins max on an A100 (fewer if other shared use). Above that, privatize into **global** per-block copies or use multi-pass binning.

## Contention model (illustrative)

Let a fraction *f* of all inputs hit the hottest bin and same-address atomics complete at roughly one per ~1 ns: serialized time ≈ f·N ns. N = 2²⁶, f = 0.9 → 60 ms; uniform data → throughput-limited ≈ memory time (~0.1-0.3 ms). Privatization moves the hot-bin serialization to shared memory (much faster and independent per block).

## Warp-aggregated atomics

When many lanes in a warp hit the *same* bin, combine them first: `mask = __match_any_sync(full, bin)`; the lane with the lowest id in the mask is the *leader*; it adds `__popc(mask)` in one atomic. Cost: a couple of warp intrinsics; benefit: up to 32× fewer atomics on skewed data. The same trick gives *stream compaction* offsets: `rank = __popc(mask & lanemask_lt)`.

## Interleaved vs contiguous coarsening

When each thread handles several inputs, assign them with **stride = total threads** (interleaved), not contiguous chunks, so a warp's loads at each step are coalesced (D1).

## Check yourself

1. Why can a non-atomic `bins[b]++` lose counts?
2. How many global atomics does the privatized version perform if there are 64 blocks and 256 bins?
3. When would privatization not fit?
4. 128 blocks, 1,024 bins: global atomics for the merge?
5. How does `__popc(mask)` reduce atomics on skewed data?
6. Why interleaved rather than contiguous per-thread chunks?

<details class="answers">
<summary>Show answers</summary>

1. read-modify-write race.
2. 16,384.
3. too many bins for shared memory.
4. 131,072.
5. one atomic per group of equal-bin lanes.
6. coalescing.

</details>

## Practice

[CU-033 Histogram](problem:CU-033)

*PMPP reference:* Ch. 9 (atomics, latency/throughput, privatization, coarsening, interleaved partitioning, aggregation).
