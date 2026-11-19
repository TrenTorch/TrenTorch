<!-- chapters: E5 -->
## 🎬 VIZ-ATOMIC-CONTENTION: "Everyone wants the same bin"
- *Canvas:* a row of bins (bars) on the right; a swarm of small thread dots on the left, each drawing an arrow to its input's bin. A queue forms in front of any bin with more than one arrow.
- *Controls:* **Number of bins** (4-256), **Data skew** slider (uniform → 90% in one bin), **Mode**: *global atomics* / *privatized in shared*, **Show lost updates** (demo with non-atomic increments).
- *Animation:* global mode: arrows pile onto a hot bin and the queue length number grows; time bar stretches. Privatized mode: each block's mini-histogram fills quickly, then a short merge phase sends one arrow per bin to the global bars.
- *Readouts:* **max queue depth**, **atomic ops on global memory**, **estimated time**.
- *Aha moment:* with uniform data both modes are fine; at 90% skew the global mode explodes while privatized barely changes.
