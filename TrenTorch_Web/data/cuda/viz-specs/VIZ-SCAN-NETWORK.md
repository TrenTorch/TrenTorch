<!-- chapters: E6 -->
## 🎬 VIZ-SCAN-NETWORK: "Two ways to prefix-sum"
- *Canvas:* 8 columns (elements) and rows representing steps, drawn as a wiring diagram. Circles are adders; arrows show where each value comes from.
- *Controls:* **Algorithm** (Hillis-Steele / Blelloch), **Input** (editable 8 numbers), `Stepper`.
- *Animation:* Hillis-Steele: each row, every column (from offset onward) adds a partner at a growing distance; counts of adders per row stay near N. Blelloch: a shrinking up-sweep tree, a root-reset to 0 flashed, then an expanding down-sweep.
- *Readouts:* **steps (depth)**, **total additions (work)**, **result**.
- *Aha moment:* for N = 8 the totals show 17 vs 14 additions: the gap grows with N.
- *Accessibility:* a table view of each step's array.
