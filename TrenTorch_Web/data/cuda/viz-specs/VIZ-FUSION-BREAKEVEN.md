<!-- chapters: F3, F6 -->
## 🎬 VIZ-FUSION-BREAKEVEN: "How much does fusion actually save?" (chapters F3, F6)
- *Canvas:* a stacked bar: GEMM time and elementwise-traffic time, with and without fusion.
- *Controls:* **Roof** (FP32 / TF32 / FP16), **Matrix size**, **Fuse** toggle.
- *Readouts:* **elementwise share of runtime** (about 5% on FP32, about 36% on TF32 in the F3 example).
- *Aha moment:* a faster GEMM makes the same fusion matter more.
