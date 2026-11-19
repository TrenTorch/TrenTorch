<!-- chapters: E1 -->
## 🎬 VIZ-MAP-FLOW: "One thread, one element"
- *Canvas:* three aligned layers: the **input array** (cells), the **thread layer** (small squares grouped into warp-coloured blocks), and the **output array**. Arrows drop from input cell → thread → output cell.
- *Controls:* **N**, **block size**, **Mode**: *one thread per element* / *grid-stride loop with fixed grid*, `Stepper`, function dropdown (ReLU, Sigmoid, GELU).
- *Animation:* in one-per-element mode all threads fire in a single wave and the idle tail threads appear hatched. In grid-stride mode a small number of threads sweep along the array in strides, each thread's visited cells lit in its own colour with a loop-counter badge.
- *Readouts:* **bytes moved = 8N**, **FLOPs**, **AI**, **bound**.
- *Aha moment:* both modes produce identical output with different thread counts.
