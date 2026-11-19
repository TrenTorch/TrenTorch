<!-- chapters: A3, B3 -->
## 🎬 VIZ-ISSUE-SLOTS: "ILP or more warps?" (chapters A3, B3)
- *Canvas:* four sub-partition scheduler rows over time; each cycle shows which warp issued (coloured), or an empty slot. Below, the pipeline of one FP32 instruction occupying 2 cycles.
- *Controls:* **Warps per scheduler** (1-16), **ILP per thread** (1, 2, 4), **Memory latency**, **Compute instructions between loads**.
- *Readouts:* **issue-slot utilization %**, **warps needed (formula from B3)**.
- *Aha moment:* 4 independent accumulators at 4 warps fill as many slots as 1 accumulator at 16 warps.
