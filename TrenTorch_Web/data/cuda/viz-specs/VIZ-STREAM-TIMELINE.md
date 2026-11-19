<!-- chapters: F2 -->
## 🎬 VIZ-STREAM-TIMELINE: "Overlap copies and compute"
- *Canvas:* three horizontal lanes: **H2D engine**, **Compute**, **D2H engine**; time on x. Chunks appear as coloured rectangles.
- *Controls:* **Number of chunks/streams** (1-8), **copy time**, **compute time**, **pinned memory** toggle.
- *Animation:* with 1 stream the rectangles go strictly left to right in a staircase. With 4 streams the lanes fill diagonally and the total length shrinks; with pinned memory off, the H2D lane blocks and the overlap disappears.
- *Readouts:* **total time**, **speed-up vs 1 stream**, **bottleneck lane**.
