<!-- chapters: F6 -->
## 🎬 VIZ-CAPSTONE-PIPELINE: "Your block, end to end"
- *Canvas:* a left-to-right dataflow diagram: `x → [matmul + bias + GELU] → h → [matmul + bias + residual] → y`. Under each node: the kernel the learner wrote (linked) and its live metrics.
- *Controls:* **Fusion level** (none / epilogue-fused), **Run all** (executes the learner's kernels in sequence in the simulator).
- *Animation:* data tokens flow through the nodes; a memory-traffic strip below swells at each global-memory write; fusion visibly deletes the intermediate write.
- *Readouts:* **total bytes**, **per-kernel bound**, **end-to-end max error vs NumPy reference**.
