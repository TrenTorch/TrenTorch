<!-- chapters: B3 -->
## 🎬 VIZ-LATENCY-HIDING: "Never wait"
- *Canvas:* a timeline: one row per warp (up to 16), time on x. Each warp's row is a sequence of coloured blocks: orange = issuing compute, blue = waiting on memory. At the bottom, a single "issue slot" row shows what the scheduler issues each cycle, and an "idle" count.
- *Controls:* **Resident warps** (1-32), **memory latency** (cycles), **compute per load** (instructions).
- *Animation:* with 1 warp the issue row is mostly empty (long blue gaps). Slide warps up: gaps fill, because each warp's wait overlaps with other warps' compute. A utilization meter climbs and plateaus.
- *Aha moment:* utilization saturates at a number of warps that depends on latency ÷ compute-per-load. Raise latency and more warps are needed to stay saturated.
