<!-- chapters: F9 -->
## 🎬 VIZ-HALO-EXCHANGE: "Cut the grid, pay the border"
- *Canvas:* a 2D grid (e.g., 24×24) split among 4 or 8 GPUs, each tile coloured; halo cells drawn as a lighter frame; arrows between neighbouring tiles.
- *Controls:* **Decomposition** (1D slabs / 2D blocks), **GPUs (2-16)**, **Stencil radius r**, **Link** (NVLink / PCIe), **Overlap comm with compute** toggle, `Stepper`.
- *Animation:* each step shows compute (tile fills), halo copy (arrows), and — with overlap on — the interior compute running at the same time as the copy, drawn on a timeline below.
- *Readouts:* **compute cells**, **halo cells**, **surface-to-volume ratio**, **time per iteration**, **comm hidden %**.
- *Aha moment:* raise GPUs with slab decomposition and the ratio climbs; switch to 2D blocks and it climbs more slowly. Toggle overlap and the iteration time drops to max(compute, comm).
