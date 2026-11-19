<!-- chapters: F4 -->
## 🎬 VIZ-RING-ALLREDUCE: "Pass it around the ring"
- *Canvas:* *p* GPU nodes on a circle, each holding a small bar chart of *p* chunks. Arrows between neighbours.
- *Controls:* **GPUs** (2-16), **Topology** (ring / NVSwitch mesh / PCIe tree), `Stepper`, **Data size**.
- *Animation:* phase 1 (reduce-scatter): coloured chunks hop one node per step and add into the receiver's matching chunk (the bar grows). Phase 2 (all-gather): finished chunks hop around until every node's chart is full. A bandwidth meter on each link shows load.
- *Readouts:* **steps = 2(p−1)**, **bytes per GPU**, **estimated time for this topology**.
- *Aha moment:* raise the GPU count and the steps go up but the bytes per GPU barely change.
- *Failure mode:* a **Skip rank** toggle shows one node refusing to participate and the others stalling with a red "waiting for rank 3".
