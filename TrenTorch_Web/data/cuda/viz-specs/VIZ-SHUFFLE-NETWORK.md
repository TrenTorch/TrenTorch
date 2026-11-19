<!-- chapters: F1 -->
## 🎬 VIZ-SHUFFLE-NETWORK: "Lanes passing notes"
- *Canvas:* 32 lanes in a row, each with a value; arcs show where each value is read from.
- *Controls:* **Intrinsic** (`shfl_down`, `shfl_xor`, `shfl` broadcast, `ballot`), **delta / mask** input, `Stepper`; a preset **Warp reduction** that runs offsets 16, 8, 4, 2, 1 in sequence.
- *Animation:* in a reduction step each lane's arc reaches `offset` lanes to the right; values add; lanes past the end get their own value back (greyed because they are not used). After five steps lane 0 shows the total, with the running partials faintly visible.
- *Aha moment:* the whole 32-lane sum finishes in five steps with no shared-memory slab in sight.
