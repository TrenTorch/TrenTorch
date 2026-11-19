<!-- chapters: F9 -->
## 🎬 VIZ-MULTIGPU-TOPOLOGY: "Who can talk to whom?"
- *Canvas:* GPUs drawn as boxes (4 or 8), links drawn between them with thickness proportional to bandwidth and colour by type (NVLink, PCIe switch, CPU bridge, cross-socket link). Two CPU sockets sit at the top.
- *Controls:* **Topology preset** (8 GPU NVSwitch / 4 GPU NVLink mesh / PCIe tree across 2 sockets), **Source GPU**, **Destination GPU**, **Data size**, **Show topo matrix** toggle.
- *Animation:* picking two GPUs lights the path hop by hop; the slowest hop is outlined as the **bottleneck**; packets stream along the path.
- *Readouts:* **hops**, **bottleneck bandwidth**, **time for D bytes**, and the code `NV12` / `PIX` / `PHB` / `SYS` for that pair; a full pairwise matrix appears when toggled.
- *Aha moment:* on the PCIe-tree preset, GPUs on opposite sockets are 10× slower to reach than neighbours, so "GPU 0 ↔ GPU 7" is not the same cost as "GPU 0 ↔ GPU 1".
- *Accessibility:* "GPU 0 to GPU 5: 3 hops, bottleneck 25 GB/s (SYS). 1 GB takes 40 ms."
- *Data note:* share the topology model with VIZ-RING-ALLREDUCE.
