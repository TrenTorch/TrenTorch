# SIMT, host and device, PCIe

## Host and device

Your program runs in two places. The **host** is the CPU and its RAM. The **device** is the GPU and its own memory (VRAM). They are separate address spaces: a pointer returned by `cudaMalloc` points into device memory and is meaningless to the CPU. A typical program allocates on the device, copies input over, launches a kernel, copies the result back.

<div class="cuda-diagram" data-diagram="cpu-gpu-system" data-title="The host, the device and the road between them"></div>

## SIMT in one paragraph

**SIMT** (Single Instruction, Multiple Threads) means the hardware issues *one* instruction and many threads execute it at once, each on its own data. You write code as if for a single thread (`out[i] = max(in[i], 0)`); the hardware groups threads into bundles of 32 called warps and runs each bundle in lockstep. It looks like SIMD (one instruction, many data lanes) but each thread has its own registers and can branch independently, at a cost you will measure in chapter C1.

## PCIe: the road between the two worlds

Copies between host and device travel over **PCIe**. A PCIe 4.0 x16 link moves roughly 25-32 GB/s each way (spec); PCIe 3.0 x16, which a T4 uses, about 12-16 GB/s. The GPU's own memory is far faster (T4: 320 GB/s, A100: ~2 TB/s).

Work an example. Copy 1 GB to an A100 over PCIe 4.0: about 40 ms. Read that same 1 GB from the A100's own memory: about 0.5 ms. The copy is nearly **80 times** slower than the thing you wanted to do with the data. Two consequences follow: copy as little as possible, and keep data on the device between kernels.

Pinned (page-locked) host memory and asynchronous copies narrow the gap a little; chapter F2 covers them.

## The lifetime of a launch

1. Host calls the kernel with `kernel<<<grid, block>>>(args)`.
2. The call returns **immediately**; the GPU works in the background (the launch is asynchronous).
3. Host synchronizes (`cudaDeviceSynchronize`) or does a blocking `cudaMemcpy`, which waits for prior work to finish.

## Interactive: The expensive highway

<div class="cuda-viz" data-viz="VIZ-HOST-DEVICE-PCIE" data-title="The expensive highway" data-spec="VIZ-HOST-DEVICE-PCIE"></div>

## Interactive: One instruction, thirty-two lanes

<div class="cuda-viz" data-viz="VIZ-SIMT-LOCKSTEP" data-title="One instruction, thirty-two lanes" data-spec="VIZ-SIMT-LOCKSTEP"></div>

## Check yourself

1. After `kernel<<<…>>>(…)` returns, is the kernel finished? How do you wait for it?
2. Why does a host pointer passed straight to a kernel not work?
3. A pipeline needs 5 kernels on the same 2 GB buffer. How many PCIe copies are needed at minimum?

<details class="answers">
<summary>Show answers</summary>

1. No; `cudaDeviceSynchronize` / blocking `cudaMemcpy` / events.
2. Separate address spaces.
3. 2 (in once, out once).

</details>

## Pitfalls

- Timing a kernel with a host clock without synchronizing; you measure only the launch.
- Re-copying data to the GPU for every kernel in a chain.

## Practice

[CU-001 Vector Addition](problem:CU-001): your first complete host → device → host round trip.
