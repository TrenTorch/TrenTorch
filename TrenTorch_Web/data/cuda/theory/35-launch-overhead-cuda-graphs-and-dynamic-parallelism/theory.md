# Launch overhead, CUDA graphs and dynamic parallelism

## Launch overhead is a fixed tax

Each kernel launch costs **≈ 3-10 µs** of host-side time and a similar-order latency before the first block starts *(approx.)*. A kernel that does 2 µs of real work is dominated by launching.
Example: a model with 1,000 tiny kernels (each 5 µs of GPU work) launched one by one: if launch is 5 µs and the GPU is idle during gaps ⇒ ≈ 5-10 ms, **half or more of it overhead**. This is why small-batch inference is "launch-bound".

## CUDA graphs

Capture a sequence of operations once (kernels, copies, dependencies) as a **graph**; launch the whole graph with one API call. Per-node launch overhead drops to ≈ 1 µs or less, and the driver can pre-plan dependencies. The 1,000-kernel example drops from ≈ 5-10 ms of overhead to ≈ 1 ms. Restriction: shapes and arguments are fixed at capture (updatable with graph-update APIs).

## Fusion vs graphs

Fusion removes **traffic and launches**; graphs remove **only launch overhead**. Use graphs when you cannot fuse (different shapes/libraries) and fusion when the intermediate traffic matters.

## Dynamic parallelism

A running kernel can launch **child grids** without returning to the host (device-side `<<<>>>`). Natural for recursion/adaptive refinement (quad-trees, adaptive mesh), where the amount of child work depends on the data. Costs: each child launch has overhead comparable to host launches, many tiny children are slower than a flat, data-parallel reformulation, and resources are reserved for pending launches. Use when the structure is truly irregular and the children are large; otherwise prefer flattening (frontier queues as in E10).

## Interactive: Gaps between kernels

<div class="cuda-viz" data-viz="VIZ-LAUNCH-OVERHEAD" data-title="Gaps between kernels" data-spec="VIZ-LAUNCH-OVERHEAD"></div>

## Check yourself

*PMPP reference:* Ch. 21 (CUDA dynamic parallelism: motivation, overhead, nested kernels, memory visibility between parent and child, streams), Ch. 22 (advanced practices: asynchronous execution and graphs context).

1. Kernel work = 3 µs, launch overhead = 5 µs, 1,000 launches: overhead share of total?
2. Name one situation where dynamic parallelism is justified and one where it is not.
3. Which reduces *memory traffic*: fusion or graphs?

<details class="answers">
<summary>Show answers</summary>

1. 5/(5+3) = 62.5% overhead.
2. justified: adaptive refinement with large children; not: many tiny children.
3. fusion.

</details>
