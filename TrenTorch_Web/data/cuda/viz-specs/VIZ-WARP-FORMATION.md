<!-- chapters: B3 -->
## 🎬 VIZ-WARP-FORMATION: "How a block is sliced into warps"
- *Canvas:* a 2D grid of thread squares (the block), up to 32×32. Threads are coloured by warp (8 repeating hues). Below it, the same threads laid out in a straight line in linearized order, with warp boundaries as thick vertical bars.
- *Controls:* **blockDim.x**, **blockDim.y** (number steppers), presets (256×1, 16×16, 8×8, 33×1, 32×4).
- *Animation:* hover a thread: its warp highlights in both views, and a tooltip shows `tid`, `warp`, `lane`. Partial warps are drawn with greyed-out empty lanes and a label "9 of 32 lanes used".
- *Readouts:* number of warps, **lane utilization %**.
- *Aha moment:* 8×8 puts four *rows* in a warp while 32×2 puts one row of 32; the second is what makes memory access contiguous (D1).
