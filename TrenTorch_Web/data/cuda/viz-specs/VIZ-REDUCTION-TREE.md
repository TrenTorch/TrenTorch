<!-- chapters: E2 -->
## 🎬 VIZ-REDUCTION-TREE: "Fold the array in half"
- *Canvas:* a binary tree drawn bottom-up from 16 input leaves to 1 root. Each node is a thread slot; at each level, active threads are filled orange, inactive ones hollow. A side panel shows the shared-memory array state at each step.
- *Controls:* **Variant** dropdown (1-6 from the ladder), **N** (16 or 32), `Stepper`, toggle **Show bank numbers**.
- *Animation:* step through levels. Variant 1: active threads are every 2nd, 4th, 8th lane, so within one warp half the lanes are masked from step one (visible divergence). Variant 3: active threads are always the *low* indices `0..s−1`, so whole warps are fully active or fully idle. Variant 2 shows red bank-conflict chips on the shared-memory strip. Variant 5 replaces the last 5 levels with arrows hopping between lanes inside one warp, with no barrier marks.
- *Readouts:* **steps**, **active lanes per step**, **warp efficiency %**, **bank conflicts**, **barriers**.
- *Aha moment:* all six variants give the same sum, but the lane-activity graph beneath the tree is wildly different.
