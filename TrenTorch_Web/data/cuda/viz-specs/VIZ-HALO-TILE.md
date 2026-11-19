<!-- chapters: E4 -->
## 🎬 VIZ-HALO-TILE: "Tile plus a halo"
- *Canvas:* a 2D input grid (e.g., 20×20). A bright tile marks the output region of one block; a lighter frame around it marks the halo; a 3×3 (or K×K) window slides inside the tile.
- *Controls:* **Filter size K** (3, 5, 7), **Tile size T**, **Mode**: *No tiling* / *Tiled with halo*, **Boundary rule**.
- *Animation:* press **Load**: tile + halo cells fly into a shared-memory panel (counter shows loads). Then the filter window sweeps the tile with no more global arrows. In *No tiling* mode every window step re-draws K² global arrows.
- *Readouts:* **loads per output**, **total global loads**, **halo overhead %**.
- *Aha moment:* grow K and the halo overhead grows; shrink T and the halo dominates, so the win vanishes.
