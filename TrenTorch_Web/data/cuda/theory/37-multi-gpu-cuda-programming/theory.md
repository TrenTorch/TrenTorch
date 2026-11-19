# Multi-GPU CUDA programming

F4 explained the *collective* (AllReduce) and its cost. This chapter covers the CUDA-level mechanics of using several GPUs: choosing a device, moving data between GPUs, splitting a problem, overlapping communication, and predicting how well it scales.

## Several devices, one host program

`cudaGetDeviceCount(&n)` reports how many GPUs the process can see. Each GPU is a separate device with its own memory, its own streams and events, and its own copy of everything in chapters A-D. Nothing is shared automatically: a pointer from `cudaMalloc` on GPU 0 belongs to GPU 0.

## Current device is thread state

`cudaSetDevice(d)` sets the **current device for the calling host thread**. Every later call on that thread (`cudaMalloc`, stream or event creation, kernel launch) targets that device until you change it. The default is device 0, so a program that forgets `cudaSetDevice` puts all its memory and work on GPU 0.
```cuda
for (int d = 0; d < nGpu; ++d) {
    cudaSetDevice(d);                       // everything below belongs to GPU d
    /* cudaMalloc(&buf[d], ...); cudaStreamCreate(&stream[d]); */
    /* kernel<<<grid, block, 0, stream[d]>>>(buf[d], ...); */   // async, returns at once
}
for (int d = 0; d < nGpu; ++d) { cudaSetDevice(d); cudaDeviceSynchronize(); }
```
Because launches are asynchronous (A2), one host thread can start work on all GPUs and they run concurrently. Rules that catch people:
- A stream or event belongs to the device that was current when it was created. Launching a kernel into another device's stream fails.
- `cudaStreamWaitEvent` **may** wait on an event recorded on another device. This is how you order work across GPUs.

## Topology: who is connected to whom

GPUs in one server are linked by **NVLink** (direct GPU-to-GPU), through an **NVSwitch** (every GPU reaches every other at full speed), or only through **PCIe** (possibly via the CPU, possibly across two CPU sockets).

| Link *(spec / approx.)* | Per-direction bandwidth |
|---|---|
| PCIe 4.0 x16 | ~25-32 GB/s |
| A100 NVLink 3 (12 links) | ~300 GB/s (600 GB/s bidirectional) |
| H100 NVLink 4 | ~450 GB/s (900 GB/s bidirectional) |
| Node-to-node InfiniBand (200 Gbit/s NIC) | ~25 GB/s |

`nvidia-smi topo -m` prints a matrix of how each pair connects: `NV#` (NVLink, # links), `PIX`/`PXB` (PCIe bridges), `PHB` (through the CPU host bridge), `SYS` (across CPU sockets). A copy between two `NV12` GPUs is about **10×** faster than between two `SYS` GPUs. Always check topology before you decide how to split work.

## Peer-to-peer access and copies

Two GPUs can touch each other's memory directly (**peer access**) when the hardware supports it.
- `cudaDeviceCanAccessPeer(&ok, a, b)` asks whether device *a* can access device *b*.
- With device *a* current, `cudaDeviceEnablePeerAccess(b, 0)` lets *a* read and write *b*'s memory. It is **one-directional**; enable both ways if you need both.
- With peer access enabled (and unified virtual addressing), a kernel on *a* may dereference a pointer into *b*'s memory. Each access then travels over the link, so it is as slow as the link and not coalescing-friendly. Prefer copying a block over the link, then computing locally.
- `cudaMemcpyPeerAsync(dst, dstDev, src, srcDev, bytes, stream)` copies GPU to GPU. With P2P it goes straight over NVLink/PCIe; **without it the driver stages through host memory** (two PCIe hops).

Calculation: 1 GB from GPU 0 to GPU 1. Direct over NVLink at 300 GB/s: 1 GB ÷ 300 GB/s ≈ **3.3 ms**. Staged through the host over PCIe 4.0 at 25 GB/s per hop: 40 ms + 40 ms = **80 ms**, about **24× slower**.

## Programming patterns

1. **One thread (or process) drives all GPUs** with the loop above. Simple, good for learning and small node counts.
2. **One process per GPU** (the norm for MPI and NCCL jobs, and for data-parallel training frameworks): each process calls `cudaSetDevice(local_rank)` once, owns one GPU, and exchanges data via NCCL or CUDA-aware MPI. Failures and driver state stay isolated per GPU, and scaling to many nodes uses the same code.
Pin each process to the CPU socket closest to its GPU (NUMA affinity); a GPU reached through the far socket sees lower copy bandwidth (the `SYS` case).

## Domain decomposition and halo exchange

To split a stencil or grid problem, give each GPU a piece of the domain. Neighbouring pieces need each other's border cells (the **halo**, as in E4) every iteration, so GPUs exchange borders.

Take a cube of side *n* per GPU with stencil radius *r*:
$$\text{halo cells} = 6\,r\,n^2,\qquad \text{compute cells} = n^3,\qquad \text{ratio} = \frac{6r}{n}$$
This is the **surface-to-volume ratio**: communication grows with the surface, compute with the volume. Bigger pieces mean relatively less communication.

Worked example: n = 512, r = 1, FP32.
- Halo bytes per exchange: 6 × 512² × 4 B = **6.3 MB**.
- Compute (memory-bound sweep reading and writing every cell): 2 × 512³ × 4 B = 1.07 GB ÷ 1.73 TB/s ≈ **0.62 ms**.
- Exchange over NVLink at 300 GB/s: 6.3 MB ÷ 300 GB/s ≈ **21 µs** (3% of compute). Over PCIe at 25 GB/s: **252 µs** (about 40% of compute).

How you cut the domain matters. A global N³ grid split into **slabs** along one axis gives each GPU halo 2rN² *regardless of p*, while compute per GPU shrinks as N³/p, so the ratio 2rp/N **grows with p**. Splitting in 3D blocks gives a ratio that grows only like p^(1/3).

## Overlapping communication with compute

Reuse the stream ideas of F2:
1. Compute the **boundary layer** first on stream A.
2. Start the halo copies on a communication stream as soon as the boundary is done.
3. Compute the **interior** on stream B at the same time.
4. Order everything with events (`cudaEventRecord`, `cudaStreamWaitEvent`).
The exchange is fully hidden when `T_comm ≤ T_interior`. In the example above, NVLink hides completely; PCIe also hides (252 µs < ~0.6 ms), but only if you actually overlap.

## Scaling: strong, weak, efficiency

- **Strong scaling:** fixed total problem, more GPUs. Speedup S(p) = T₁ / T_p, efficiency E(p) = S(p) / p.
- **Weak scaling:** work per GPU fixed, problem grows with p. Efficiency E_w = T₁ / T_p (ideal 1).
A useful model: `T_p = T_serial + T_par / p + T_comm(p)`.

Worked example: T₁ = 100 ms of parallel work, gradient AllReduce of 5.8 ms (F4 example).
- 8 GPUs, no overlap: T₈ = 12.5 + 5.8 ≈ 18.3 ms ⇒ S = 5.5, **E = 68%**.
- 8 GPUs, communication fully overlapped with backward compute: T₈ ≈ max(12.5, 5.8) = 12.5 ms ⇒ S = 8, E = 100% (ideal case).
Amdahl (A5) still applies: any serial part, including host-side work and launch gaps (F7), caps strong scaling.

## Worked example: matrix multiply on 4 GPUs

Split C = A × B by **rows of A** across p GPUs and replicate B (N = 8,192, FP32, p = 4).
- Compute per GPU: 2 · (N/p) · N² = 275 GFLOP ⇒ ≈ **17.6 ms** at 15.6 TFLOPS (80% of 19.5).
- Communication: broadcast B, N² × 4 B = 268 MB ⇒ ≈ **0.9 ms** at 300 GB/s (≈ 5% of compute).
- As p grows, compute per GPU shrinks like 1/p but each GPU still needs all of B, so efficiency falls. A **2D decomposition** (SUMMA-style) cuts per-GPU communication to about N²/√p words.

## Multi-GPU pitfalls

| Bug | Symptom | Fix |
|---|---|---|
| Forgot `cudaSetDevice` | GPU 0 runs out of memory while others idle | set the device before every allocation and launch on that thread |
| Pointer used on the wrong device | illegal access or wrong data | track which device owns each pointer |
| Peer access not enabled | illegal access, or a copy 10-20× slower than expected | `cudaDeviceCanAccessPeer` + `cudaDeviceEnablePeerAccess`, both directions if needed |
| Stream/event from another device | launch error | create each stream/event while its device is current |
| Mismatched collectives | hang (F4) | all ranks call the same collectives, order and sizes |
| Load imbalance | scaling flattens | split by cost, not by element count |
| Unordered cross-GPU float sums | results differ in last digits | compare with a tolerance (E2) |

## Beyond one node

Across nodes the same ideas hold with a slower link (InfiniBand ~25 GB/s per NIC) and more latency. **CUDA-aware MPI** and **GPUDirect RDMA** let a NIC read GPU memory directly, avoiding a host copy. The hierarchy (NVLink inside a node, network between nodes) is why collective libraries do a local reduce first, then a cross-node step.

## Interactive: Who can talk to whom?

<div class="cuda-viz" data-viz="VIZ-MULTIGPU-TOPOLOGY" data-title="Who can talk to whom?" data-spec="VIZ-MULTIGPU-TOPOLOGY"></div>

## Interactive: Direct or via the host?

<div class="cuda-viz" data-viz="VIZ-P2P-ACCESS" data-title="Direct or via the host?" data-spec="VIZ-P2P-ACCESS"></div>

## Interactive: Which GPU is current?

<div class="cuda-viz" data-viz="VIZ-DEVICE-CONTEXT" data-title="Which GPU is current?" data-spec="VIZ-DEVICE-CONTEXT"></div>

## Interactive: Cut the grid, pay the border

<div class="cuda-viz" data-viz="VIZ-HALO-EXCHANGE" data-title="Cut the grid, pay the border" data-spec="VIZ-HALO-EXCHANGE"></div>

## Interactive: Where does scaling bend?

<div class="cuda-viz" data-viz="VIZ-SCALING-CURVE" data-title="Where does scaling bend?" data-spec="VIZ-SCALING-CURVE"></div>

## Check yourself

1. What does `cudaSetDevice(2)` change, and for which thread?
2. A kernel on GPU 0 dereferences a pointer allocated on GPU 1 and fails. Name two things to check.
3. Cube pieces of side n = 256, radius 1: what fraction of cells is halo?
4. Why does a slab decomposition scale worse than a 3D block decomposition as p grows?
5. When is a halo exchange fully hidden by overlap?

<details class="answers">
<summary>Show answers</summary>

1. the current device for the calling host thread; later allocations, streams, events and launches on that thread target GPU 2.
2. peer access not enabled in that direction (or unsupported by the topology), and the pointer's owning device.
3. 6/256 = **2.3%**.
4. slab halo stays 2rN² while compute per GPU shrinks like 1/p, so the ratio grows with p; 3D blocks grow only like p^(1/3).
5. when T_comm ≤ T_interior (communication fits under the interior compute).

</details>

## Pitfalls

- Assuming all GPU pairs have the same bandwidth.
- Measuring multi-GPU time without synchronizing every device.
- Using the default device everywhere and wondering why only GPU 0 is busy.

## Practice

[CU-047 Multi-GPU AllReduce](problem:CU-047) · [CU-051 Bug Hunt: NCCL Deadlock](problem:CU-051)
<div class="coming-soon"><div class="cs-head"><strong>CU-057 Multi-GPU halo exchange</strong><span class="cs-badge">Coming soon</span></div><p>1D stencil split over 2-4 simulated GPUs; the report shows halo bytes, link time, and overlap</p></div>

*PMPP reference:* Ch. 20 (programming a heterogeneous cluster: domain partitioning, halo exchange, overlapping communication with computation, CUDA-aware MPI), Ch. 22 (advanced practices and multi-GPU context). **Not in PMPP:** NVLink/NVSwitch bandwidth figures and `nvidia-smi topo` notation: cite NVIDIA architecture whitepapers and the CUDA Programming Guide.

## Further reading

- NVIDIA CUDA C++ Programming Guide, multi-device and peer-to-peer sections; NVIDIA A100/H100 architecture whitepapers (NVLink/NVSwitch)
- Van de Geijn & Watts, "SUMMA: Scalable Universal Matrix Multiplication Algorithm" (1997)
