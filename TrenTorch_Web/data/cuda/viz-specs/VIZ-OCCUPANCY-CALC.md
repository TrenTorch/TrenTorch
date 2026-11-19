<!-- chapters: B4 -->
## 🎬 VIZ-OCCUPANCY-CALC: "What limits me?"
- *Canvas:* four horizontal bars (threads, blocks, registers, shared memory), each showing how much of the SM's budget the current configuration uses *per block*, stacked to show how many blocks fit. The tightest bar is outlined in red and labelled **limiter**. A big dial shows occupancy %.
- *Controls:* **Block size**, **registers/thread**, **shared memory/block**, **Profile** (T4 / A100).
- *Animation:* drag registers/thread from 32 up to 128; the register bar fills faster, the number of fitting blocks steps down (8 → 4 → 2), the dial falls in discrete jumps, and the limiter label switches from "threads" to "registers".
- *Aha moment:* the dial changes in *steps*, not smoothly, and the answer differs between T4 and A100.
