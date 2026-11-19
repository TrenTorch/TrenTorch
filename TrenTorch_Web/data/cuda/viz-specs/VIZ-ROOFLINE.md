<!-- chapters: D2 -->
## 🎬 VIZ-ROOFLINE: "Where does my kernel live?"
- *Canvas:* a log-log plot. x: arithmetic intensity (FLOP/byte, 0.01 → 1000). y: performance (GFLOP/s). A sloped line (memory roof) meets a flat line (compute roof) at the ridge point, which is labelled. Kernels are dots with names.
- *Controls:* **Profile** (T4 / A100 / H100 / RTX 4090), checkboxes for preset kernels (vector add, ReLU, SAXPY, softmax, naive matmul, tiled matmul T=16/32), **drag handle** to create a custom kernel by AI, and **Show my last run** (reads counters from the problem workspace).
- *Animation:* switching profile slides the ridge point left or right; tiling a matmul (T = 1 → 32) makes the dot climb diagonally up the memory roof toward the ridge. A shaded region left of the ridge is labelled **memory-bound**, right of it **compute-bound**.
- *Readouts:* for the selected dot: AI, attainable GFLOP/s, **% of roof**, bound classification, estimated time (from the model).
- *Aha moment:* ReLU sits far left of the ridge on every GPU; moving to a faster-arithmetic GPU does nothing for it, but moving to higher bandwidth does.
- *Accessibility:* "ReLU: 0.125 FLOP/byte, memory-bound. Ridge on A100 is 9.6."
