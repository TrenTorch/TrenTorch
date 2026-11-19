<!-- chapters: D4 -->
## 🎬 VIZ-SHARED-BOUND: "The hidden bottleneck in tiling" (chapter D4)
- *Canvas:* two pipes feeding an FMA block: shared-memory loads (128 B/cycle) and FMA issue (2 warp-FMAs/cycle). Counters show cycles needed for each.
- *Controls:* **Register tile R** (1, 2, 4, 8), **Profile**.
- *Animation:* at R = 1 the load pipe is saturated (4× the FMA time) and the FMA block idles 75%; at R = 4 both pipes are balanced.
- *Readouts:* **loads per warp-FMA = 2/R**, **limiting resource**, **% of FMA peak**.
- *Aha moment:* the bottleneck moves from shared bandwidth to compute at R = 4.
