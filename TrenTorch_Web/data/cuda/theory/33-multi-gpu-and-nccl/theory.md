# Multi-GPU and NCCL

## Why more than one GPU

Models and datasets outgrow one GPU, and training is faster in parallel. The standard scheme, **data parallelism**: each GPU holds a copy of the model, processes its own slice of the batch, computes gradients, and then **all GPUs average their gradients** so the copies stay identical. That average is a collective operation called **AllReduce**.

## NCCL and collectives

NCCL is the library for GPU collectives. Core operations: **AllReduce**, **Broadcast**, **AllGather**, **ReduceScatter**, **AllToAll**, point-to-point **Send/Recv**.

## Ring AllReduce

Arrange the *p* GPUs in a ring and split the data into *p* chunks.
1. **Reduce-scatter** (p−1 steps): each step every GPU sends one chunk to its neighbour and adds the chunk it receives, so each GPU ends up owning the full sum of one chunk.
2. **All-gather** (p−1 steps): the finished chunks travel around the ring until everyone has all of them.
Total steps 2(p−1). Each GPU sends about $2 \cdot \frac{p-1}{p} \cdot D$ bytes for data size D, which is nearly independent of *p*: the algorithm is **bandwidth-optimal** and scales well.

## Topology matters

A fast all-to-all fabric (NVLink + NVSwitch) vs a ring vs a PCIe tree through the host changes the effective bandwidth by a large factor (the simulator models these topologies).

## Deadlocks

Every rank must call the same collectives in the same order with matching sizes. If rank 3 skips a call, or calls `AllReduce` with a different count, the others wait forever. The simulator detects rank, count and ordering mismatches and reports the offending rank.

## Interactive: Pass it around the ring

<div class="cuda-viz" data-viz="VIZ-RING-ALLREDUCE" data-title="Pass it around the ring" data-spec="VIZ-RING-ALLREDUCE"></div>

## The α-β cost model

Time to send *n* bytes over one link: `T = α + n/β` with latency α (≈ 5-10 µs) and bandwidth β.
- **Ring AllReduce**, *p* GPUs, data size D:
$$T_{\text{ring}} = 2(p-1)\,\alpha + 2\,\frac{p-1}{p}\cdot\frac{D}{\beta}$$
- **Tree AllReduce** (reduce up + broadcast down, double-binary-tree in NCCL):
$$T_{\text{tree}} \approx 2\log_2 p\cdot\alpha + c\cdot\frac{D}{\beta}$$
Ring is **bandwidth-optimal** (volume factor → 2 as p grows, not growing with p) but has latency growing linearly with p; trees have latency O(log p). Small messages ⇒ tree/latency-optimized; large messages ⇒ ring/bandwidth-optimized. NCCL picks automatically.

## Worked example: gradients of a 250 M-parameter model (FP32 ⇒ D = 1 GB)

- **8 GPUs, NVLink**, β = 300 GB/s per direction *(A100 NVLink3 ≈ 600 GB/s bidirectional)*: bandwidth term = 2 × (7/8) × 1 GB ÷ 300 GB/s = **5.8 ms**; latency term = 14 × 5 µs = 0.07 ms ⇒ **≈ 5.9 ms**.
- **8 GPUs over PCIe 4.0** (β ≈ 25 GB/s through the host/switch): 1.75 GB ÷ 25 GB/s = **70 ms**: 12× slower.
- **Per-GPU bytes sent** with p = 2: D; p = 8: 1.75 D; p = 64: 1.97 D; p → ∞: 2 D (**nearly constant**).
If the backward pass takes 100 ms, a 5.9 ms AllReduce can be **fully overlapped** (gradient buckets are reduced as soon as they are ready, while earlier layers are still computing), whereas 70 ms cannot be hidden entirely.

## Reduce-scatter and all-gather separately

ReduceScatter + AllGather = AllReduce. Sharded optimizers (ZeRO / FSDP) keep gradients and optimizer state **sharded** and use only ReduceScatter then AllGather of *parameters* when needed, trading extra communication steps for memory. Volume per GPU: ReduceScatter ≈ (p−1)/p · D, AllGather ≈ (p−1)/p · D.

## Parallelism flavours in one table

| Scheme | What is split | Communication |
|---|---|---|
| Data parallel | batch | AllReduce of gradients |
| Tensor parallel | each weight matrix (columns/rows) | AllReduce/AllGather of activations *inside* every layer (needs NVLink-class bandwidth) |
| Pipeline parallel | layers into stages | point-to-point activations between stages; bubbles |
| Sharded data parallel (FSDP/ZeRO) | params/grads/optimizer state | AllGather + ReduceScatter |

## Interactive: Ring or tree?

<div class="cuda-viz" data-viz="VIZ-ALPHA-BETA" data-title="Ring or tree?" data-spec="VIZ-ALPHA-BETA"></div>

## Check yourself

1. Why is each GPU's total traffic nearly constant as *p* grows?
2. What causes an NCCL deadlock from a mismatched call order?
3. Which collective is used to sum gradients across data-parallel replicas?
4. Ring AllReduce time for D = 400 MB, p = 4, β = 50 GB/s (ignore latency)?
5. Why do tensor-parallel layers need faster links than data-parallel gradient sync?
6. Which two collectives compose into an AllReduce?

<details class="answers">
<summary>Show answers</summary>

1. volume per GPU → 2D.
2. ranks disagree on collective order/size.
3. AllReduce.
4. 2·(3/4)·400 MB = 600 MB ⇒ 12 ms.
5. per-layer, on the critical path, with activation-sized messages.
6. ReduceScatter + AllGather.

</details>

## Practice

[CU-047 Multi-GPU AllReduce](problem:CU-047) · [CU-051 Bug Hunt: NCCL Deadlock](problem:CU-051)

*PMPP reference:* Ch. 20 (programming a heterogeneous cluster: MPI, halo exchange, overlapping communication and computation, CUDA-aware MPI). **Not in PMPP:** NCCL's ring/tree implementation details and FSDP/ZeRO: cite NCCL docs and the ZeRO paper.

## Further reading

- NVIDIA CUDA C++ Programming Guide and Best Practices Guide; NCCL documentation
