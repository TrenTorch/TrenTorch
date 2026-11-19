<!-- chapters: F3 -->
## 🎬 VIZ-FUSION-TRAFFIC: "Count the round trips"
- *Canvas:* a pipeline diagram of 3-4 operations drawn as boxes. Between each pair: an arrow to and from a "global memory" bar at the bottom (unfused), versus arrows staying in a "registers" strip (fused).
- *Controls:* **Pipeline preset** (bias+ReLU, matmul+bias+GELU, scale+mask+softmax), **Fuse** toggle, **Tensor size**.
- *Animation:* toggling **Fuse** deletes the intermediate arrows with a satisfying collapse; a byte counter and a time bar shrink.
- *Readouts:* **bytes moved**, **estimated time**, **traffic saved %**.
- *Second panel (attention):* an N × N square scales with N; toggle **Flash-style tiling** to replace it with a small sliding tile and a running (m, d) badge; the memory number drops from O(N²) to O(N).
