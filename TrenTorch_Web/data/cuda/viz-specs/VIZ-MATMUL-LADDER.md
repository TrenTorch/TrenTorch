<!-- chapters: E7 -->
## 🎬 VIZ-MATMUL-LADDER: "Climb the ladder"
- *Canvas:* a horizontal scrubber with seven stops (v1…v7). Above it, a panel for the selected version: the three matrices with one block's footprint outlined; arrows from global memory (thickness proportional to bytes). Below: a mini roofline with a dot per version and a bar chart of global loads, shared bytes, and estimated time.
- *Controls:* **Version scrubber**, **Matrix size** (e.g., 64/128/256), **Profile**; a **Run in simulator** button that fills the bars from real counters for versions the learner has solved.
- *Animation:* dragging the scrubber morphs the picture: v1 shows every thread pulling its own row/column (a forest of arrows); v3 shows tile-sized blue arrows into a shared slab; v4/v6 show each thread owning a small block of C; v7 shows two shared slabs alternating.
- *Readouts:* **global loads**, **shared-memory bytes**, **bank conflicts**, **AI**, **estimated time (modelled)**.
- *Aha moment:* the bars shrink at every step and the roofline dot climbs, with the "why" sentence under each stop.
