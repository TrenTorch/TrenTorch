<!-- chapters: A4 -->
## 🎬 VIZ-SCOPE-VISIBILITY: "Who can see what?"
- *Canvas:* a grid of 2 blocks × 6 threads. Each thread tile shows a mini register chip; each block has a shared-memory slab beneath; one big global slab spans the bottom.
- *Controls:* click any thread to **select** it; choose **Operation: read / write**; choose a target memory.
- *Animation:* a selected thread draws lines to everything it can reach (own registers, its block's shared slab, global). Reachable items highlight green; the other block's shared slab and other threads' registers stay red with a "not visible" tag.
- *Aha moment:* thread (block 1, thread 2) cannot touch block 0's shared memory at all.
