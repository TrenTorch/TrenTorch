<!-- chapters: C1 -->
## 🎬 VIZ-DIVERGENCE-LANES: "Both roads, one after the other"
- *Canvas:* top: a row of 32 `LaneStrip` squares with each lane's input value printed beneath (e.g., `-3, 2, -1, 5, …`). Middle: two "code panels" side by side, **Path A** (`out = x`) and **Path B** (`out = 0`). Bottom: a cycle timeline with a ruler, and a bar **"cycles used" vs "cycles if no divergence"**.
- *Controls:* **Data pattern** (all positive, all negative, alternating, random 50/50, first 16 positive), **Code form** toggle (**branchy** / **branchless fmaxf**), `Stepper`.
- *Animation (branchy):* step 1, the 32 lanes evaluate the condition; step 2, lanes that chose A flash orange while lanes for B go hollow-hatched; the Path A panel highlights. Step 3, the roles swap. Step 4, all lanes return to filled and a "reconverge" marker appears. The timeline shows two segments. *Animation (branchless):* one segment, all 32 lanes filled throughout.
- *Readouts:* **active lanes per step**, **warp efficiency %** (average active lanes ÷ 32), cycles used.
- *Aha moment:* with *all positive* data the branchy form runs only one path (no cost), with *alternating* data it runs both; the branchless form never changes. A small note appears: "The compiler may turn the branchy form into predicated code. This model shows the divergent case."
- *Accessibility:* "Pass 1 of 2: lanes 1, 3, 5… active (16 of 32). Pass 2 of 2: lanes 0, 2, 4… active."
