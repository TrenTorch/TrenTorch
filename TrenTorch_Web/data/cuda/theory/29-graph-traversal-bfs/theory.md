# Graph traversal (BFS)

## The problem

Breadth-first search computes the distance (in edges) from a source vertex to every other vertex. It is **irregular** (the amount of work per level depends on the graph), **data-dependent** (memory addresses come from edge lists), and **low-arithmetic** (almost pure memory traffic).

## Level-synchronous BFS

Maintain a **frontier** (vertices discovered at the current level). Each iteration visits every neighbour of every frontier vertex; unvisited neighbours join the next frontier. One kernel launch per level; the launch boundary is the global barrier that blocks cannot provide themselves (B2).

## Parallelization choices

1. **Vertex-centric, push:** one thread per *frontier vertex* iterates over its edges, marking neighbours with `atomicCAS(&dist[v], INF, level+1)` so each vertex is claimed once. Imbalance: a high-degree vertex's thread runs long (loop divergence, C1).
2. **Vertex-centric, pull (bottom-up):** one thread per *unvisited* vertex scans its neighbours looking for **any** frontier member and stops at the first hit. Much cheaper when the frontier is huge (most vertices are about to be visited).
3. **Edge-centric:** one thread per edge; perfectly balanced work but scans all edges every level (wasteful in early/late levels).
4. **Direction-optimizing:** push while the frontier is small, pull when it is large: a standard choice in modern GPU BFS.

## Building the next frontier

Threads append discovered vertices to a shared queue. Contended `atomicAdd` on one tail pointer is a hotspot; use **block-local queues** (shared-memory counters, privatization from E5) and a block-level merge, or **warp-aggregated** appends (E5). With scan (E6) you can compute exact write offsets without atomics on the queue.

## The numbers

Per edge traversed: read the neighbour id (4 B, coalescable within an adjacency list), read/CAS `dist[v]` (random 4 B access = a full 32 B sector, 12.5% efficient). So ≈ 4 + 32 = **~36 B moved per edge** for ≈ 1 useful operation. A graph with 10⁹ edges ⇒ ≈ 36 GB ⇒ ≈ 21 ms at 1.7 TB/s *(lower bound for a single full-graph sweep)*. Graph analytics performance is measured in **TEPS** (traversed edges per second); the bandwidth model above caps it near 10¹⁰ TEPS on an A100 *(illustrative)*.

## Why graphs are hard on GPUs

Power-law degree distributions (a few vertices with millions of edges), random memory access (no coalescing), and frontier sizes that vary by orders of magnitude between levels. The remedy theme is the same as everywhere: sort/bucket by degree, cooperate across lanes (warp- or block-per-vertex for heavy vertices), and keep the frontier compact.

## Interactive: Level by level

<div class="cuda-viz" data-viz="VIZ-BFS-FRONTIER" data-title="Level by level" data-spec="VIZ-BFS-FRONTIER"></div>

## Check yourself

1. Why must `dist[v]` be claimed atomically in push-style BFS?
2. When is bottom-up (pull) cheaper than top-down?
3. Why is one kernel launch per BFS level a natural fit for level-synchronous BFS?

<details class="answers">
<summary>Show answers</summary>

1. two threads may discover the same vertex.
2. when the frontier is large.
3. the launch boundary is the global barrier.

</details>

## Proposed problem

<div class="coming-soon"><div class="cs-head"><strong>CU-054 BFS (level-synchronous, push)</strong><span class="cs-badge">Coming soon</span></div><p>report shows atomics, lane utilization, bytes per edge.</p></div>

*PMPP reference:* Ch. 15 (graph traversal: vertex-centric push/pull, edge-centric, frontier-based, privatization of frontiers, load balancing).

## Further reading

- Merrill, Garland, Grimshaw, "Scalable GPU Graph Traversal" (2012)
