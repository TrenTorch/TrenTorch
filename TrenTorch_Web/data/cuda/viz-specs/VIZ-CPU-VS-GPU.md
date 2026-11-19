<!-- chapters: A1 -->
## 🎬 VIZ-CPU-VS-GPU: "Two kinds of processor"
- *Canvas:* two floorplans side by side. Left: a CPU die drawn as 4 large core tiles, each surrounded by big cache blocks and a control block (about 60% of the area is cache and control, shown in grey). Right: a GPU die drawn as a grid of dozens of small SM tiles, each filled with tiny orange dots (cores), with a thin strip of cache.
- *Controls:* a segmented toggle **Workload: One long dependent task | 10,000 independent tasks**, and a **Run** button.
- *Animation:* a progress bar under each chip. With *one long task*, the CPU finishes first (the GPU's single thread is slower; most GPU dots stay dark). With *10,000 independent tasks*, CPU cores light up four at a time and the bar crawls, while thousands of GPU dots light up and the GPU bar finishes much earlier. A running label shows tasks completed per second for each.
- *Aha moment:* the same toggle flips the winner, so "GPUs are faster" becomes "GPUs are faster *for this shape of work*".
- *Accessibility:* text readout "CPU: 4 tasks at a time, 1.0 s each. GPU: 2,560 tasks at a time, 3.0 s each."
