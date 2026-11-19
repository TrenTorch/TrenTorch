<!-- chapters: B4 -->
## 🎬 VIZ-OCCUPANCY-STAIRCASE (extension of VIZ-OCCUPANCY-CALC)
- *Canvas:* x: registers/thread (16 → 255); y: occupancy %. A staircase curve for the chosen block size; marker for the user's current setting; second curve for the other GPU profile.
- *Controls:* **Block size**, **Shared memory/block**, **Show granularity rounding** toggle.
- *Aha moment:* between two stair edges, adding registers is *free*; one register past an edge costs a whole block.
