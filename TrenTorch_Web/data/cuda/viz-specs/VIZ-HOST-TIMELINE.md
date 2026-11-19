<!-- chapters: B5 -->
## 🎬 VIZ-HOST-TIMELINE: "Who is waiting for whom?"
- *Canvas:* two timeline lanes: **Host** (top) and **Device** (bottom), time on x.
- *Controls:* toggles **Insert cudaDeviceSynchronize after launch**, **Use blocking cudaMemcpy**, number of launches (1-4).
- *Animation:* the host lane issues tiny "launch" ticks immediately and moves on; the device lane shows kernel bars running after a small gap. Without sync, a host `printf` of the result appears *before* the kernel bar ends and is marked red "reads stale data". With sync, the host lane shows a hatched "waiting" bar until the kernel ends.
- *Aha moment:* launches are cheap and asynchronous; the host only waits when you tell it to (or when you do a blocking copy).
