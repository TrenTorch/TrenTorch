<!-- chapters: F9 -->
## 🎬 VIZ-SCALING-CURVE: "Where does scaling bend?"
- *Canvas:* speedup (y) vs number of GPUs (x, 1-64) with the ideal line dashed; a shaded gap shows the loss; second panel shows efficiency %.
- *Controls:* **Mode** (strong / weak), **Serial fraction** slider, **Comm model** (none / constant AllReduce / ring AllReduce with α-β), **Link**, **Overlap** toggle.
- *Animation:* dragging any control redraws the curve; the point where efficiency drops below 80% is marked.
- *Readouts:* **speedup**, **efficiency**, **comm share of step time** at the selected GPU count.
- *Aha moment:* with constant communication and no overlap, strong scaling flattens early; overlap pushes the bend far to the right.
