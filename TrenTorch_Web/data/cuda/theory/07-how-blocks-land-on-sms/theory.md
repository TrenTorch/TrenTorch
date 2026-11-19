# How blocks land on SMs

## Blocks are independent

The GigaThread Engine assigns each block to an SM and the block stays there until it finishes. Two rules follow, and you must design for both:
1. **No ordering.** Block 7 may run before block 0, or at the same time. Never assume order.
2. **No cooperation across blocks** within a kernel. Blocks cannot wait for each other. To combine results across blocks use atomics (E5) or a second kernel.

This independence is what lets the same program run on a 20-SM laptop GPU and a 132-SM data-center GPU: more SMs simply means more blocks at once.

<div class="cuda-diagram" data-diagram="block-scheduling" data-title="Blocks handed to SMs"></div>

## Residency

An SM holds several blocks at the same time, as many as its registers, shared memory and thread slots allow. All resident blocks' warps compete for the SM's schedulers. A block that is not resident waits in the queue.

## Waves and the tail effect

Suppose a GPU can hold 864 blocks at once (108 SMs × 8 blocks each, hypothetical). A grid of 1,000 blocks runs in two "waves": 864 in the first, only 136 in the second. In the second wave most SMs idle, so average utilization is 1000 / (2 × 864) ≈ **58%**. A grid of 1,728 blocks fills both waves perfectly. This **tail effect** is why a very small grid, or an awkward size, can underuse the machine. Grid-stride loops (D-chapters and plan §E1) are one fix.

## Interactive: Blocks find a home

<div class="cuda-viz" data-viz="VIZ-BLOCK-SCHEDULER" data-title="Blocks find a home" data-spec="VIZ-BLOCK-SCHEDULER"></div>

## Check yourself

1. Can block 3 read a value block 2 wrote earlier in the same kernel? Why not?
2. A grid has 100 blocks and the GPU can run 108 at once. What is wasted?
3. Why is "independent blocks" good for portability?

<details class="answers">
<summary>Show answers</summary>

1. No ordering or residency guarantee.
2. 8 slots idle (7%).
3. the same program maps to any SM count.

</details>

## Practice

[CU-001 Vector Addition](problem:CU-001): run with different block sizes and read the report.
