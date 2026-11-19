<!-- chapters: A2 -->
## 🎬 VIZ-HOST-DEVICE-PCIE: "The expensive highway"
- *Canvas:* left, a box labelled **CPU + RAM**; right, a box labelled **GPU + VRAM**; between them a horizontal road labelled **PCIe**. The road's width is drawn proportional to bandwidth, and a much fatter pipe connects the GPU core to its VRAM inside the GPU box.
- *Controls:* **Data size** slider (1 MB → 8 GB), **GPU profile** dropdown (T4 / A100 / H100), **PCIe generation** (3.0 / 4.0 / 5.0), a checkbox **Keep data on device between kernels**.
- *Animation:* press **Play**: orange packets stream along the PCIe road (host→device), then fast green packets move inside the GPU while a kernel runs, then packets stream back. A Gantt strip below shows three bars: *copy in*, *compute*, *copy out*, with their durations.
- *Readouts:* time for each phase and "**PCIe is X× slower than on-device memory**".
- *Aha moment:* tick **Keep data on device** with 10 chained kernels; the Gantt strip collapses from 20 copy bars to 2.
- *Accessibility:* readout sentence "Copy in: 41 ms. Compute: 0.5 ms. Copy out: 41 ms."
