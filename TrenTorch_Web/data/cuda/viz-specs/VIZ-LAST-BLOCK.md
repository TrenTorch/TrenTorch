<!-- chapters: C3 -->
## 🎬 VIZ-LAST-BLOCK: "Who finishes last?"
- *Canvas:* 6 blocks as columns; each draws "write partial", optional "fence", "ticket". A global counter and a `partial[]` array below.
- *Controls:* **Include `__threadfence()`** toggle; `Stepper`; **Reorder visibility** toggle (forces block 3's write to arrive late).
- *Animation:* without the fence and with reordering enabled, the final block reads `partial[3]` as stale (red "stale read"); with the fence, the write is visible before the ticket increments.
- *Aha moment:* the atomic ticket tells you *who is last*; only the fence guarantees *what they can see*.
