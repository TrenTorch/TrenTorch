<!-- chapters: A4 -->
## 🎬 VIZ-MEMORY-LADDER: "The memory pyramid"
- *Canvas:* a vertical pyramid, five coloured bands (the fixed tints). Each band is labelled with size, latency and bandwidth. Right side: a clock-like latency bar for each band drawn to a log scale.
- *Controls:* **Profile** dropdown; **Send a load** button; hover a band for scope text.
- *Animation:* press **Send a load of a value that is only in global memory**: a dot travels from the top (register) down to the bottom (global), sits there with a ticking cycle counter, then rides back up leaving copies in L2 and L1. Press it again: the dot now stops at L1 and returns in ~30 cycles. Then **Evict**: the copies vanish.
- *Aha moment:* the same load costs 20× different amounts depending on where the data already lives.
