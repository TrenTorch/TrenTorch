<!-- chapters: E10 -->
## 🎬 VIZ-BFS-FRONTIER: "Level by level"
- *Canvas:* a graph (up to 40 nodes; presets: grid, random, star-with-hub, power-law) with nodes coloured by level; below it a bar chart of **frontier size per level** and a `LaneStrip` showing which lanes own frontier vertices.
- *Controls:* **Strategy** (push / pull / direction-optimizing), `Stepper`, **Source vertex**.
- *Readouts:* **edges examined per level**, **atomic claims**, **lane utilization**.
- *Aha moment:* on the hub graph, push explodes at one level (one thread does all the work) while pull examines far fewer edges at the big middle level.
