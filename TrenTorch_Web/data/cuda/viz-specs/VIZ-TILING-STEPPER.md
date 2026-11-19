<!-- chapters: D4 -->
## 🎬 VIZ-TILING-STEPPER: "Load once, use many times"
- *Canvas:* three matrices drawn as grids: **A** (left), **B** (top), **C** (bottom right). A coloured T×T tile outlines the active block's output region in C, a matching horizontal strip in A and vertical strip in B. A "shared memory" panel below shows two small T×T slabs `As`, `Bs`.
- *Controls:* **Matrix size** (e.g., 8×8 to 32×32), **Tile size T** (2, 4, 8, 16), **Mode**: *Naive* / *Tiled*; `Stepper`.
- *Animation (tiled):* step 1: the active tile of A and B light up and copy into the slabs (arrows from global cells to shared cells). Step 2: barrier flash. Step 3: T partial products accumulate into the C tile (cells darken a little each step). Step 4: barrier flash, then the next tile along K slides in. *(Naive mode:* every C cell draws its own full row/column of arrows.)
- *Readouts:* **global loads so far**, **loads if naive**, **reduction factor** (should equal T), **shared bytes used**.
- *Aha moment:* flip between modes and watch the global-load counter differ by exactly T.
- *Accessibility:* "Tile 2 of 4: loaded 32 values into shared memory; 256 multiply-adds done; global loads so far: 64 vs 512 naive."
