<!-- chapters: F4 -->
## 🎬 VIZ-ALPHA-BETA: "Ring or tree?" (chapter F4)
- *Canvas:* time vs message size (log-log) for ring and tree AllReduce, with the crossover marked.
- *Controls:* **GPUs p**, **α**, **β**, **Message size**.
- *Readouts:* **T_ring**, **T_tree**, **winner**.
- *Aha moment:* small messages are latency-bound (tree wins); large messages are bandwidth-bound (ring wins).
