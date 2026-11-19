<!-- chapters: F9 -->
## 🎬 VIZ-P2P-ACCESS: "Direct or via the host?"
- *Canvas:* two GPU boxes with a host box between them; code panel on the left listing `cudaSetDevice`, `cudaDeviceEnablePeerAccess`, and a `cudaMemcpyPeerAsync`.
- *Controls:* checkbox **Peer access enabled (0→1)**, checkbox **Peer access enabled (1→0)**, a **Kernel on GPU 0 reads GPU 1 memory** button, **Copy size**.
- *Animation:* with access off, a copy visibly goes GPU1 → host → GPU0 (two hops, two time bars). With access on, one direct hop. The kernel-read button shows a red "illegal access" chip if access is off, or small packets over the link if on.
- *Readouts:* **copy time**, **hops**, **speed-up of direct vs staged**.
- *Aha moment:* peer access is directional; enabling 0→1 does not allow 1→0.
