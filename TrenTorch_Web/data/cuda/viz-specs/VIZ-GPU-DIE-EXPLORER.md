<!-- chapters: A3 -->
## 🎬 VIZ-GPU-DIE-EXPLORER: "Zoom into the GPU"
- *Canvas:* a die floorplan. Top bar: **GigaThread Engine**. Left/right edges: memory controllers connected to memory chips. Centre: a grid of GPC rectangles, each containing SM tiles. Bottom: PCIe interface. A breadcrumb shows **GPU › GPC › SM › Sub-partition**.
- *Controls:* mouse wheel or **＋/−** to zoom; click any unit to open a side card with its name, one-sentence definition, and a link into the glossary; **Profile** dropdown (T4 / A100 / H100) changes how many GPCs/SMs are drawn and updates the counts.
- *Animation:* press **Launch a grid**. The GigaThread Engine emits small numbered squares (blocks) that fly into SM tiles; SM tiles fill up (a bar shows resource use) and show a "full" state; as blocks finish, new ones are dispatched.
- *Zoom levels:* (1) whole die; (2) one GPC with its SMs; (3) one SM with four sub-partitions and a shared-memory/L1 block; (4) one sub-partition with scheduler, register file, core grid, LD/ST, SFU.
- *Aha moment:* when zoomed into an SM, a block of threads shows as warps (rows of 32 dots) pinned to the SM's sub-partitions.
- *Accessibility:* every unit is a focusable button; Enter opens its definition.
