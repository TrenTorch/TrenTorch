# Streams and overlap

## The idea

A **stream** is an ordered queue of GPU work. Operations in one stream run in order; operations in different streams may overlap. Modern GPUs have separate engines for copies and for compute, so a copy for chunk *k+1* can run while the kernel for chunk *k* runs.

## Requirements

- Use **pinned (page-locked) host memory** (`cudaMallocHost`) so copies can be asynchronous.
- Use `cudaMemcpyAsync` with an explicit stream, and launch the kernel into that stream.
- Split the data into chunks, and give consecutive chunks different streams.

## What you gain

Without overlap the total is *copy-in + compute + copy-out*. With S chunks and overlap the total approaches the **longest** of the three plus a small pipeline fill/drain cost. If copying dominates (PCIe is slow, A2), overlap hides compute; if compute dominates it hides copies.

## Limits

More streams than needed add overhead. Overlap only helps when there is something to overlap (large enough work, independent chunks). The browser simulator may not model all stream behaviour, so this chapter is a model-driven visualization plus text.

## Interactive: Overlap copies and compute

<div class="cuda-viz" data-viz="VIZ-STREAM-TIMELINE" data-title="Overlap copies and compute" data-spec="VIZ-STREAM-TIMELINE"></div>

## The pipeline time formula

Split work into *S* equal chunks. Per-chunk times: copy-in h = H/S, compute k = K/S, copy-out d = D/S. With enough engines and ideal overlap:
$$T(S) \approx (h + k + d) + (S-1)\cdot\max(h, k, d)$$
(first chunk fills the pipeline, then one chunk completes every max(·).)
Example: H = D = 40 ms, K = 10 ms, S = 4: h = d = 10, k = 2.5 ⇒ T = 22.5 + 3 × 10 = **52.5 ms** vs 90 ms serial (1.7×). Lower bound = max(H, K, D) = 40 ms. As S → ∞ the formula approaches 40 ms plus per-chunk overheads. Each extra chunk adds launch/sync overhead (~10-20 µs), so there is a sweet spot (often 4-16 chunks).
Note: H2D and D2H use separate copy engines on most data-center GPUs, but both share the PCIe link's *directional* bandwidth only with their own direction, so full-duplex overlap of in/out is realistic; with only one copy engine the in/out copies serialize and the formula's `max` becomes `max(h + d, k)`.

## Which stream rules matter

- Same stream ⇒ ordered; different streams ⇒ no order unless you add events (`cudaEventRecord` / `cudaStreamWaitEvent`).
- The default stream has legacy synchronizing behaviour unless you use per-thread default streams.
- Pageable memory is staged through a pinned buffer by the driver, so the copy cannot be fully asynchronous.

## Check yourself

1. Why must host memory be pinned for async copies to overlap?
2. Copy = 40 ms, compute = 10 ms, 4 chunks. Roughly how long with perfect overlap?
3. H = D = 60 ms, K = 20 ms, S = 6: T(S)?
4. What changes if the GPU has one copy engine?

<details class="answers">
<summary>Show answers</summary>

1. async DMA needs page-locked pages.
2. 52.5 ms (lower bound 40).
3. h = d = 10, k = 3.33 ⇒ T = 23.3 + 5 × 10 = 73.3 ms (serial: 140 ms).
4. in/out copies serialize.

</details>

*PMPP reference:* Ch. 20 (CUDA streams, overlapping data transfer and computation in the heterogeneous-cluster chapter), Ch. 22 (advanced practices; asynchronous operations).
