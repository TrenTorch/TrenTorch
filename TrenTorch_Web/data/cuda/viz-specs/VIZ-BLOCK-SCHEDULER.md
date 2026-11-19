<!-- chapters: B2 -->
## 🎬 VIZ-BLOCK-SCHEDULER: "Blocks find a home"
- *Canvas:* left, a queue of numbered block tokens. Centre: a grid of SM tiles, each drawn with 4-8 empty slots. Right: a utilization graph over time.
- *Controls:* **#SMs** (4-132), **blocks per SM**, **grid size** (blocks), **time per block** (uniform or random). **Play/Step**.
- *Animation:* tokens leave the queue and drop into free slots; when a block finishes (slot turns green and empties), the next token drops in. Tokens are numbered, and the finishing order is visibly *not* sorted.
- *Readouts:* wave count, overall utilization %, idle-SM time in the last wave.
- *Aha moment:* slide grid size from 864 to 1000 and utilization falls; slide to 1728 and it jumps back up. A toggle **Random block times** shows blocks completing out of order.
