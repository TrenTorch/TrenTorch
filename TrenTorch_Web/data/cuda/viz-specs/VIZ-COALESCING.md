<!-- chapters: D1 -->
## 🎬 VIZ-COALESCING: "From 32 addresses to transactions"
- *Canvas:* top: a `LaneStrip` of 32 lanes, each lane with an arrow pointing down to a memory strip. The memory strip is drawn as a long row of cells (4 bytes each) grouped into 32-byte sectors (alternating tint) and 128-byte lines (bold dividers).
- *Controls:* **Stride** slider (1, 2, 4, 8, 32), **Offset** slider (0-31 elements), **Element size** (4 B float / 16 B float4), **Layout preset** (contiguous, AoS 12-byte struct, column of a row-major matrix).
- *Animation:* press **Issue load**: the 32 arrows land; every sector that contains at least one requested byte lights up orange; requested bytes inside lit sectors are bright, unrequested bytes are dim. A counter ticks up the number of sectors fetched.
- *Readouts:* **transactions (sectors) = 4**, **bytes moved = 128**, **bytes useful = 128**, **efficiency = 100%**, with the numbers recomputing live.
- *Aha moment:* drag the offset from 0 to 1 and efficiency drops from 100% to 80%; drag the stride to 32 and it collapses to 12.5%, with a mountain of dim bytes.
- *Accessibility:* "Stride 2: 8 sectors fetched, 128 of 256 bytes useful (50%)."
