<!-- chapters: F7 -->
## 🎬 VIZ-LAUNCH-OVERHEAD: "Gaps between kernels"
- *Canvas:* a timeline with **Host** and **Device** lanes; N kernels as bars on the device lane with gaps equal to launch overhead.
- *Controls:* **Kernels (1-200)**, **GPU time per kernel**, **Launch overhead**, **Mode** (individual launches / CUDA graph / fused into one).
- *Readouts:* **total time**, **% overhead**, **GPU utilization**.
- *Aha moment:* for 5 µs kernels, "graph" and "fused" collapse the gaps; for 5 ms kernels all three modes are indistinguishable.
