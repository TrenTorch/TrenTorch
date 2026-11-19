<!-- chapters: A5 -->
## 🎬 VIZ-PERF-CALCULATOR: "Predict before you run"
- *Canvas:* left, a form of inputs; right, a live "receipt" showing each term of the time model as a coloured bar (memory term blue, compute term orange, launch term grey) with the winner outlined.
- *Controls:* **Profile**, **Bytes per element**, **FLOPs per element**, **N** (log slider), **η_m** and **η_c** sliders (defaults 0.85 / 0.8), **Data starts on host** checkbox (adds PCIe terms), **Kernels run (k)**.
- *Animation:* sliding **k** from 1 to 8 with *data starts on host* ticked shows the GPU/CPU crossover marker sliding to the left of k = 3.
- *Readouts:* t_mem, t_compute, t_launch, bound, AI, % of roofline, and "CPU vs GPU" winner.
- *Aha moment:* worked example 2 reproduced live; ReLU shows memory ≈ 75× compute.
- *Accessibility:* sentence readout "Memory term 1.24 ms, compute term 0.014 ms, launch 0.005 ms. Memory-bound."
