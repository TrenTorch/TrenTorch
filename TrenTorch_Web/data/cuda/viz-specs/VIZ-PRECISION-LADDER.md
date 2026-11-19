<!-- chapters: F8 -->
## 🎬 VIZ-PRECISION-LADDER: "Same sum, four formats"
- *Canvas:* a number line with the representable values of the chosen format near the current value (spacing visible); a bar for "error".
- *Controls:* **Format**, **Operation** (sum of N ones, dot product, softmax of logits), **Accumulator precision**, **N**.
- *Animation:* the FP32 accumulator stalls at 16,777,216 when adding ones; FP16 stalls at 2,048 (spacing becomes 2 above 2¹¹). Switching the accumulator to a wider type fixes it.
- *Readouts:* **result**, **true value**, **relative error**, **bytes moved**.
- *Aha moment:* FP16 "sum of ones" gives 2,048, **stops 98% early on a 100,000-element sum**.
