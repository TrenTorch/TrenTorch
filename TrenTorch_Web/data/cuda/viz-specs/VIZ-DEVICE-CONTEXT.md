<!-- chapters: F9 -->
## 🎬 VIZ-DEVICE-CONTEXT: "Which GPU is current?"
- *Canvas:* a host-thread timeline of API calls; below it, one memory bar per GPU (4 GPUs).
- *Controls:* toggle **Call cudaSetDevice before each allocation**, **Number of buffers**, **Buffer size**, `Stepper`.
- *Animation:* without `cudaSetDevice` every allocation lands on GPU 0 and its bar fills to the top and turns red ("out of memory") while GPUs 1-3 stay empty; with it, bars fill evenly.
- *Aha moment:* "the current device is state on the calling thread", visible as a highlighted GPU that changes only when you call `cudaSetDevice`.
