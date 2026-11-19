<!-- chapters: B1 -->
## 🎬 VIZ-INDEX-CALCULATOR: "Who am I?"
- *Canvas:* top: a row of block rectangles (blocks 0…G−1), each containing small thread squares. Bottom: a strip of the data array, one cell per element, aligned under the threads.
- *Controls:* number inputs **N**, **blockDim.x**, and a computed **gridDim.x**; a toggle **Show bounds check**; click any thread square to pin it.
- *Animation:* click a thread: a formula card appears: `idx = 1 × 4 + 2 = 6`, the numbers colour-matched to their sources (blockIdx purple, blockDim blue, threadIdx orange). A line drops from the thread to its element cell. If `idx ≥ N`, the line ends in a red ✖ "outside the array" and the thread is drawn hollow (idle).
- *Presets:* "N=6, block=4" (the worked example), "N=1000, block=256" (shows 24 idle tail threads).
- *Aha moment:* change **N** to a multiple of the block size and the idle threads disappear.
- *Accessibility:* "Thread 2 of block 1 maps to element 6, which is outside the array (N = 6); it does nothing."
