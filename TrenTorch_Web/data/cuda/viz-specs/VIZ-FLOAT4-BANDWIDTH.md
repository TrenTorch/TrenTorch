<!-- chapters: D3 -->
## 🎬 VIZ-FLOAT4-BANDWIDTH: "Does wider help?"
- *Canvas:* top: a line chart. x: array size (log, 1 KB → 1 GB); y: effective bandwidth (GB/s). Three lines: `float`, `float2`, `float4`. A dashed horizontal line marks the GPU's peak bandwidth. Bottom: a schematic of one warp issuing `float` (32 × 4 B) next to one issuing `float4` (32 × 16 B), with the instruction counts beside them.
- *Controls:* **Source toggle**: *Measured on T4 (Colab)* / *Simulator model*; **Alignment** toggle (aligned / offset by 4 B, which shows the fallback); **Operation** (copy, ReLU, SAXPY).
- *Animation:* switching source redraws the lines; the "measured" source shows a provenance badge (GPU name, CUDA version, date, median of N runs) and error bars. The warp schematic animates a load as 1 wide block vs 4 thin ones.
- *Aha moment:* small arrays are launch-dominated (lines overlap); large arrays separate the lines near the bandwidth ceiling; misalignment makes the float4 line lose its advantage.
- *Data note for the agent:* the "measured" series is a static JSON committed from the Colab notebook; the viz must never imply that simulator timings are T4 measurements.
- *Accessibility:* a table view of the plotted numbers.
