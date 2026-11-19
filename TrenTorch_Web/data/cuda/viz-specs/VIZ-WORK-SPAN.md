<!-- chapters: A1 -->
## 🎬 VIZ-WORK-SPAN: "How parallel is this problem?" (chapter A1)
- *Canvas:* a dependency graph drawn left to right. Nodes are operations; edges are dependencies. Presets: array add (N independent nodes), tree sum (log levels), Fibonacci chain.
- *Controls:* **Preset**, **N**, **Processors p** slider.
- *Animation:* nodes light up level by level; with p processors only p nodes run per step.
- *Readouts:* **work W**, **span S**, **parallelism W/S**, **time on p processors ≥ max(W/p, S)**.
- *Aha moment:* the Fibonacci chain stays at parallelism 1 however large p is.
