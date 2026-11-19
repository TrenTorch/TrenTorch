<!-- chapters: E6 -->
## 🎬 VIZ-SCAN-LOOKBACK: "Single-pass scan" (chapter E6)
- *Canvas:* blocks as columns, each with a status flag (not ready / aggregate / inclusive prefix) and arrows looking back at predecessors.
- *Controls:* **Blocks (4-12)**, **Random scheduling order**, `Stepper`.
- *Animation:* each block publishes its aggregate, then walks back until it finds an inclusive prefix, then publishes its own.
- *Readouts:* **look-back steps per block**, **global words moved: 2N vs 3N-4N for multi-pass**.
- *Aha moment:* waiting only on lower-numbered blocks never deadlocks.
