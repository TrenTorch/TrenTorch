<!-- chapters: E3 -->
## 🎬 VIZ-ROWWISE-SOFTMAX: "One block per row"
- *Canvas:* a small matrix (4 rows × 16 cols). Row 1 is expanded below into a strip of 16 values assigned to 8 threads (two values each). Under the strip: three stacked stage panels *max → exp & sum → divide*.
- *Controls:* **Mode**: *3-pass stable* / *naive unstable* / *online 1-pass*; **Logit scale** slider (1 → 100); `Stepper`.
- *Animation:* in *naive unstable* mode with large logits, `exp` cells turn red with "inf" and the output row becomes NaN. In *3-pass* mode three sweeps of arrows scan the row. In *online* mode a single sweep carries a small (m, d) badge that updates; at the end threads merge their badges in a mini tree.
- *Readouts:* **passes over the row**, **bytes read**, max abs error vs a reference.
- *Aha moment:* slide the logit scale up and the unstable mode breaks while the other two stay identical.
