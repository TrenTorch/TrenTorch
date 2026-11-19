# Inside the chip

Zoom into a GPU and the same pattern repeats at every level: a few shared services at the top, many identical workers below.

## The tree

<div class="cuda-diagram" data-diagram="chip-hierarchy" data-title="Inside a GPU"></div>

## The GigaThread Engine

The top-level scheduler. When you launch a grid, it takes the list of thread blocks and assigns each one to an SM that has room, then assigns more as blocks finish. It never splits a block across SMs.

## The SM: the unit that matters

Everything you do in CUDA is shaped by the SM. Per SM you have a fixed budget of **registers** (typically 65,536 32-bit registers), **shared memory** (tens to ~200 KB), **thread slots** (1,024 on Turing/T4, 2,048 on Ampere/A100) and **block slots**. A block can only run on an SM that can fit *all* of its threads' registers and its shared memory. Those budgets are why "occupancy" (chapter B4) exists.

Inside an SM, four **sub-partitions** each have a **warp scheduler**. Each cycle, each scheduler picks one ready warp and issues one instruction for it. So an SM can issue instructions for up to four warps per cycle.

## CUDA cores, SFUs, tensor cores

- **CUDA core**: a simple FP32 (or INT32) arithmetic unit. Many per SM: 64 on a T4 SM, 64 on an A100 SM, 128 on many consumer chips.
- **SFU**: special-function unit for fast approximate `sin`, `cos`, `exp2`, `rsqrt`. This is what `__expf` uses (chapter E1).
- **Load/Store units**: move data between registers and the memory system.
- **Tensor cores**: matrix-multiply-accumulate units for small tiles of low-precision numbers. We explain them for context but the simulator does not model them.

## The memory side

Below the SMs sits an **L2 cache** shared by all SMs (T4: 4 MB, A100: 40 MB *(spec)*), then the **memory controllers** that connect to GDDR6 (T4) or HBM (A100, H100).

## Three profiles side by side *(spec)*

| | T4 | A100 | H100 SXM |
|---|---|---|---|
| SMs | 40 | 108 | 132 |
| FP32 cores | 2,560 | 6,912 | 16,896 |
| Memory | 16 GB GDDR6, 320 GB/s | 80 GB HBM2e, ~2,039 GB/s | 80 GB HBM3, ~3,350 GB/s |
| L2 | 4 MB | 40 MB | 50 MB |

## Interactive: Zoom into the GPU

<div class="cuda-viz" data-viz="VIZ-GPU-DIE-EXPLORER" data-title="Zoom into the GPU" data-spec="VIZ-GPU-DIE-EXPLORER"></div>

## Instruction throughput per SM, from the specs

A100 SM: four sub-partitions, each with **16 FP32 lanes** *(spec)*. A warp has 32 threads, so one FP32 warp instruction occupies a sub-partition for **2 cycles**. Per SM that is 4 warps issued per 2 cycles = 2 warp-FMAs per cycle = 64 FMA/cycle/SM, which matches "64 FP32 cores per SM".

Consequences you can calculate:
- A100 SM peak = 64 FMA × 2 FLOP × 1.41 GHz = **180 GFLOP/s per SM**; × 108 SMs = 19.5 TFLOPS ✓.
- To keep the FP32 pipes full each sub-partition must issue an FP32 instruction every 2 cycles. If a warp has no ready instruction (waiting on memory or on its own dependency), the slot is wasted unless another warp is ready.
- **Instruction-level parallelism (ILP)** gives *independent instructions inside one thread* (e.g., four independent accumulators). It fills the pipeline with fewer warps, which is why a kernel at 25% occupancy with ILP 4 can match one at 100% occupancy with ILP 1 (see B4).

## Other throughput facts *(approx., A100)*

| Unit | Per SM per cycle |
|---|---|
| FP32 FMA | 64 |
| INT32 | 64 |
| FP64 | 32 |
| SFU (`__expf`, `rsqrtf` approx.) | 16 |
| Load/store (shared memory) | 32 lanes × 4 B = 128 B |

The shared-memory line, **128 B/cycle/SM**, is the figure we use in chapter D4 to show that naive tiling is *shared-memory-bound*.

## The L2 and DRAM view

DRAM is accessed in bursts; the GPU's memory transaction granularity is the **32-byte sector** (D1). L2 sits between the SMs and DRAM; a hit in L2 avoids DRAM traffic entirely and is why measured "effective" bandwidth can exceed DRAM bandwidth for small working sets. Use **DRAM bytes** (not L2 bytes) when you compute AI for a roofline.

## Interactive: ILP or more warps?

<div class="cuda-viz" data-viz="VIZ-ISSUE-SLOTS" data-title="ILP or more warps?" data-spec="VIZ-ISSUE-SLOTS"></div>

## Check yourself

1. Who decides which SM a block runs on?
2. Can one block use two SMs?
3. Which unit would execute `__expf(x)`?
4. How many cycles does one FP32 warp instruction occupy a 16-lane sub-partition?
5. Why can ILP substitute for occupancy?

<details class="answers">
<summary>Show answers</summary>

1. GigaThread Engine.
2. No.
3. SFU.
4. 2 cycles.
5. independent instructions in one warp keep the pipe full with fewer warps.

</details>

## Pitfalls

- Picturing "CUDA cores" as independent processors. They are lanes controlled by the warp schedulers.

*PMPP reference:* Ch. 4 (architecture, scheduling, warp issue, latency tolerance), Ch. 6 (memory transaction granularity and coalescing).
