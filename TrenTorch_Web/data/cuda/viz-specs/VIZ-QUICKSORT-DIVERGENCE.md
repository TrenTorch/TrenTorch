<!-- chapters: E8 -->
## 🎬 VIZ-QUICKSORT-DIVERGENCE: "Partitioning a warp"
- *Canvas:* top: an array of 32 values assigned to 32 lanes, with a pivot value shown. Middle: the `LaneStrip` with active/masked states. Bottom: a **lane-utilization-over-time** graph and a small recursion tree whose nodes are sized by partition length.
- *Controls:* **Array shape** (random, sorted, many duplicates), **Algorithm** (quicksort / bitonic), `Stepper`.
- *Animation:* quicksort: lanes with value < pivot go "left" (orange), others masked, then roles swap; utilization hovers near 50%. The recursion tree grows lopsided for sorted input. Bitonic: a sweep of aligned compare-exchange arrows; all 32 lanes stay active in every stage.
- *Readouts:* **average lane utilization %**, **stages/steps**, **max recursion depth** (quicksort).
- *Aha moment:* sorted input makes the quicksort tree a long skinny chain (bad pivots), while bitonic does not care about the input at all.
