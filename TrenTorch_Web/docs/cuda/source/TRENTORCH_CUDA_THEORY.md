# TrenTorch CUDA: Theory Content (all chapters, with visualization specs)

> Companion to `TRENTORCH_CUDA_SECTION_PLAN.md`. Chapter IDs (A1…F6), problem IDs (CU-xxx), visualization IDs (VIZ-…) and section anchors match that plan, so the build-time link validator can resolve them.
> Each chapter has: **the theory**, **a 🎬 visualization spec** (what the learner sees and does), **check yourself**, **pitfalls**, and **practice links**.

## How to use this file (for the agent)

1. Each `# CHAPTER` block becomes one MDX file `content/cuda/theory/<ID>-<slug>.mdx`. Convert the metadata line to frontmatter (see plan §2.2).
2. Every `##` heading is a **section anchor** (slugified by `rehype-slug`). Problems link to those slugs, for example `#branchless-vs-divergence`. **Do not rename headings** without updating `meta.json` files.
3. Each `🎬` block is the **spec** for a React component in `components/cuda/viz/<id>/`. Build the pure-TypeScript model first, then the view.
4. Code in theory chapters is **deliberately partial** (`/* ... */`). The complete versions belong to the problem solutions, so reading theory never spoils a problem.
5. Numbers marked *(approx.)* vary by GPU generation; the viz must read them from the GPU-profile JSON, not hard-code them. Numbers marked *(spec)* come from published specs and are the same in the profile JSON.
6. All prose here is original. The PMPP book is referenced only by chapter number for further reading.

## Visual language (shared by every viz)

| Thing | Look |
|---|---|
| Active lane / thread | Filled TrenTorch orange ⚡ square |
| Masked (inactive) lane | Hollow square with grey diagonal hatch |
| Waiting on memory (stalled warp) | Blue, with a small clock glyph |
| Memory cell touched now | Bright outline, pulse once |
| Bank conflict / race / out-of-bounds | Red, plus an icon and a text label (never colour alone) |
| Registers / shared / L1 / L2 / global | Five fixed tints from warm (fast, small) to cool (slow, large); the same tints in every viz |
| Time axis | Always left → right; one tick = one instruction issue unless labelled |

Shared primitives to build once: `LaneStrip` (32 squares), `MemoryGrid` (cells with addresses), `Stepper` (play / pause / step / reset / speed), `ReadoutBar` (live numbers), `TermChip` (hover → glossary). Every viz offers *reduced motion* (steps instead of animation) and an `aria-live` sentence describing the current state.

---

# CHAPTER A1: Why GPUs exist
`id: A1 · part: A · est: 15 min · prereqs: none · problems: none · pmpp: Ch. 1`

## The two ways to build a fast processor

A processor can be fast in two different senses. **Latency**: finish *one* task as quickly as possible. **Throughput**: finish *as many tasks as possible per second*. A CPU is built for latency. It spends most of its silicon on cleverness: deep caches, branch prediction, out-of-order execution. All of that exists so that one stream of instructions never has to wait. A GPU is built for throughput. It spends most of its silicon on arithmetic units and accepts that any single thread is slow, because it keeps thousands of threads in flight and always has something else to do while one of them waits.

Think of a CPU as a few brilliant chefs who each cook a full meal quickly, and a GPU as a huge kitchen line where hundreds of cooks each chop one vegetable. For one dinner, the chefs win. For ten thousand salads, the line wins.

## What "data parallel" means

A problem suits a GPU when you apply **the same operation to a lot of independent data**: add two vectors, apply ReLU to every activation, multiply matrices. The element at position 7 does not need the result for position 6. If you have done the TrenTorch NumPy modules, you have already written code like this; `np.maximum(x, 0)` is the same operation applied to every element, and the GPU does it with one thread per element.

## Rough numbers (spec)

| | CPU (server class) | GPU (T4) | GPU (A100) |
|---|---|---|---|
| Parallel arithmetic lanes | tens to ~100 cores | 2,560 FP32 cores | 6,912 FP32 cores |
| Main memory bandwidth | ~50-100 GB/s | 320 GB/s | ~2,039 GB/s |
| Strength | latency, branching, irregular work | throughput, regular math | throughput, regular math |

The GPU gap is about an order of magnitude in memory bandwidth and two orders in parallel lanes. That bandwidth is what you will spend the rest of this course learning to use well.

## When a GPU does not help
Small problems (launch and copy costs dominate), problems with long dependency chains (step *n* needs step *n−1*), and heavily branching irregular code. The later chapters on divergence and sorting show exactly why.

## 🎬 VIZ-CPU-VS-GPU: "Two kinds of processor"
- *Canvas:* two floorplans side by side. Left: a CPU die drawn as 4 large core tiles, each surrounded by big cache blocks and a control block (about 60% of the area is cache and control, shown in grey). Right: a GPU die drawn as a grid of dozens of small SM tiles, each filled with tiny orange dots (cores), with a thin strip of cache.
- *Controls:* a segmented toggle **Workload: One long dependent task | 10,000 independent tasks**, and a **Run** button.
- *Animation:* a progress bar under each chip. With *one long task*, the CPU finishes first (the GPU's single thread is slower; most GPU dots stay dark). With *10,000 independent tasks*, CPU cores light up four at a time and the bar crawls, while thousands of GPU dots light up and the GPU bar finishes much earlier. A running label shows tasks completed per second for each.
- *Aha moment:* the same toggle flips the winner, so "GPUs are faster" becomes "GPUs are faster *for this shape of work*".
- *Accessibility:* text readout "CPU: 4 tasks at a time, 1.0 s each. GPU: 2,560 tasks at a time, 3.0 s each."

## Check yourself
1. A job adds two arrays of 10 million floats. CPU or GPU? Why?
2. A job computes the next Fibonacci number from the previous two, a million times in a row. CPU or GPU? Why?
3. True or false: a GPU thread is faster than a CPU thread.

## Pitfalls
- Assuming "more cores" always means faster. The workload must have enough independent work to keep them busy.

---

# CHAPTER A2: SIMT, host and device, PCIe
`id: A2 · part: A · est: 25 min · prereqs: A1 · problems: CU-001 · pmpp: Ch. 2`

## Host and device
Your program runs in two places. The **host** is the CPU and its RAM. The **device** is the GPU and its own memory (VRAM). They are separate address spaces: a pointer returned by `cudaMalloc` points into device memory and is meaningless to the CPU. A typical program allocates on the device, copies input over, launches a kernel, copies the result back.

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

## 🎬 VIZ-HOST-DEVICE-PCIE: "The expensive highway"
- *Canvas:* left, a box labelled **CPU + RAM**; right, a box labelled **GPU + VRAM**; between them a horizontal road labelled **PCIe**. The road's width is drawn proportional to bandwidth, and a much fatter pipe connects the GPU core to its VRAM inside the GPU box.
- *Controls:* **Data size** slider (1 MB → 8 GB), **GPU profile** dropdown (T4 / A100 / H100), **PCIe generation** (3.0 / 4.0 / 5.0), a checkbox **Keep data on device between kernels**.
- *Animation:* press **Play**: orange packets stream along the PCIe road (host→device), then fast green packets move inside the GPU while a kernel runs, then packets stream back. A Gantt strip below shows three bars: *copy in*, *compute*, *copy out*, with their durations.
- *Readouts:* time for each phase and "**PCIe is X× slower than on-device memory**".
- *Aha moment:* tick **Keep data on device** with 10 chained kernels; the Gantt strip collapses from 20 copy bars to 2.
- *Accessibility:* readout sentence "Copy in: 41 ms. Compute: 0.5 ms. Copy out: 41 ms."

## 🎬 VIZ-SIMT-LOCKSTEP: "One instruction, thirty-two lanes"
- *Canvas:* a column of pseudo-assembly lines on the left (`LD r1, [in+i]`, `MAX r2, r1, 0`, `ST [out+i], r2`) with a pointer arrow; right, a `LaneStrip` of 32 lanes, each lane showing its own register values for `r1`, `r2` and its own `i`.
- *Controls:* `Stepper`. A data pattern dropdown: *all positive*, *alternating*, *random*.
- *Animation:* the pointer moves down one instruction per step; on each step all 32 lanes flash together and their register cells update with different values.
- *Aha moment:* same instruction, different data per lane. No lane is ahead of the others.
- *Accessibility:* "Instruction 2 of 3: MAX executed by 32 of 32 lanes."

## Check yourself
1. After `kernel<<<…>>>(…)` returns, is the kernel finished? How do you wait for it?
2. Why does a host pointer passed straight to a kernel not work?
3. A pipeline needs 5 kernels on the same 2 GB buffer. How many PCIe copies are needed at minimum?

## Pitfalls
- Timing a kernel with a host clock without synchronizing; you measure only the launch.
- Re-copying data to the GPU for every kernel in a chain.

## Practice
[CU-001 Vector Addition](problem:CU-001): your first complete host → device → host round trip.

---

# CHAPTER A3: Inside the chip
`id: A3 · part: A · est: 30 min · prereqs: A2 · problems: none (glossary-heavy) · pmpp: Ch. 4`

Zoom into a GPU and the same pattern repeats at every level: a few shared services at the top, many identical workers below.

## The tree
```
GPU
├─ GigaThread Engine         (global scheduler: hands thread blocks to SMs)
├─ PCIe interface, memory controllers, L2 cache, HBM/GDDR channels
└─ GPCs (Graphics Processing Clusters)
   └─ TPCs (Texture Processing Clusters, 2 SMs each in recent chips)
      └─ SMs (Streaming Multiprocessors)  ← where your code actually runs
         └─ 4 sub-partitions ("processing blocks")
            ├─ 1 warp scheduler + dispatch unit
            ├─ register file
            ├─ FP32 cores (and INT32, FP64 on some chips), tensor cores
            ├─ load/store units, special-function units (SFU)
            └─ (shared per SM) L1 cache / shared memory
```

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

## 🎬 VIZ-GPU-DIE-EXPLORER: "Zoom into the GPU"
- *Canvas:* a die floorplan. Top bar: **GigaThread Engine**. Left/right edges: memory controllers connected to memory chips. Centre: a grid of GPC rectangles, each containing SM tiles. Bottom: PCIe interface. A breadcrumb shows **GPU › GPC › SM › Sub-partition**.
- *Controls:* mouse wheel or **＋/−** to zoom; click any unit to open a side card with its name, one-sentence definition, and a link into the glossary; **Profile** dropdown (T4 / A100 / H100) changes how many GPCs/SMs are drawn and updates the counts.
- *Animation:* press **Launch a grid**. The GigaThread Engine emits small numbered squares (blocks) that fly into SM tiles; SM tiles fill up (a bar shows resource use) and show a "full" state; as blocks finish, new ones are dispatched.
- *Zoom levels:* (1) whole die; (2) one GPC with its SMs; (3) one SM with four sub-partitions and a shared-memory/L1 block; (4) one sub-partition with scheduler, register file, core grid, LD/ST, SFU.
- *Aha moment:* when zoomed into an SM, a block of threads shows as warps (rows of 32 dots) pinned to the SM's sub-partitions.
- *Accessibility:* every unit is a focusable button; Enter opens its definition.

## Check yourself
1. Who decides which SM a block runs on?
2. Can one block use two SMs?
3. Which unit would execute `__expf(x)`?

## Pitfalls
- Picturing "CUDA cores" as independent processors. They are lanes controlled by the warp schedulers.

---

# CHAPTER A4: The memory hierarchy at a glance
`id: A4 · part: A · est: 20 min · prereqs: A3 · problems: CU-001 · pmpp: Ch. 5`

## A ladder, not a single memory
A GPU has several kinds of memory. Small ones are fast and private; large ones are slow and shared. Almost all CUDA performance work is *moving data to a faster rung and reusing it there*.

| Memory | Scope (who can see it) | Where it lives | Latency *(approx.)* | Size *(approx.)* |
|---|---|---|---|---|
| Registers | one thread | SM register file | ~1 cycle | up to 255 per thread, 64K per SM |
| Shared memory | one block | on the SM | ~20-30 cycles | 48-164 KB per SM (configurable) |
| L1 cache | one SM | on the SM | ~30 cycles | shares space with shared memory |
| L2 cache | all SMs | chip-wide | ~200 cycles | 4-50 MB |
| Global memory | whole grid, and the host | VRAM (GDDR/HBM) | ~400-800 cycles | 16-80 GB |
| Local memory | one thread | *physically in global memory* | like global | spilled registers, big arrays |
| Constant memory | whole grid, read-only | VRAM + dedicated cache | fast if all lanes read the same address | 64 KB |

Latency and size are approximate and differ by chip; the viz reads them from the profile.

## Scope is a contract
A variable in a register belongs to one thread; threads cannot read each other's registers (except with warp shuffles, F1). Shared memory is declared with `__shared__` and is visible to every thread in the same block, and *only* that block. Global memory is the only place blocks can exchange data during a kernel, and only through atomics or by ending the kernel.

## Why this matters
A global load costs hundreds of cycles; a floating-point add costs a handful. If every operand comes from global memory, the arithmetic units wait most of the time. The programmer's job is to use each byte loaded from global memory **as many times as possible** before it is evicted from the fast rungs. Chapters D1-D6 teach how.

## 🎬 VIZ-MEMORY-LADDER: "The memory pyramid"
- *Canvas:* a vertical pyramid, five coloured bands (the fixed tints). Each band is labelled with size, latency and bandwidth. Right side: a clock-like latency bar for each band drawn to a log scale.
- *Controls:* **Profile** dropdown; **Send a load** button; hover a band for scope text.
- *Animation:* press **Send a load of a value that is only in global memory**: a dot travels from the top (register) down to the bottom (global), sits there with a ticking cycle counter, then rides back up leaving copies in L2 and L1. Press it again: the dot now stops at L1 and returns in ~30 cycles. Then **Evict**: the copies vanish.
- *Aha moment:* the same load costs 20× different amounts depending on where the data already lives.

## 🎬 VIZ-SCOPE-VISIBILITY: "Who can see what?"
- *Canvas:* a grid of 2 blocks × 6 threads. Each thread tile shows a mini register chip; each block has a shared-memory slab beneath; one big global slab spans the bottom.
- *Controls:* click any thread to **select** it; choose **Operation: read / write**; choose a target memory.
- *Animation:* a selected thread draws lines to everything it can reach (own registers, its block's shared slab, global). Reachable items highlight green; the other block's shared slab and other threads' registers stay red with a "not visible" tag.
- *Aha moment:* thread (block 1, thread 2) cannot touch block 0's shared memory at all.

## Check yourself
1. Which memory can two different blocks both write to during a kernel?
2. What is "local memory" really?
3. Why do the fastest memories have the smallest size?

## Practice
[CU-001 Vector Addition](problem:CU-001): count which levels a load and a store touch.

---

# CHAPTER B1: Threads, blocks, grids and indexing
`id: B1 · part: B · est: 30 min · prereqs: A2 · problems: CU-001, CU-002, CU-009, CU-010 · pmpp: Ch. 2-3`

## Three nested levels
A launch creates a **grid** of **blocks**, each block holding **threads**. You choose the shape:
```cuda
kernel<<<gridDim, blockDim>>>(...);
```
Inside the kernel, built-in variables tell a thread who it is: `threadIdx` (position in its block), `blockIdx` (position of its block in the grid), `blockDim` (threads per block), `gridDim` (blocks in the grid). Each has `.x`, `.y`, `.z`.

## The global index
For a 1D layout:

$$\text{idx} = \text{blockIdx.x} \times \text{blockDim.x} + \text{threadIdx.x}$$

Think of blocks as pages of a notebook with `blockDim.x` lines each: `blockIdx.x` is the page, `threadIdx.x` the line, `idx` the line number counted from the start of the notebook.

## Sizing the grid
To cover `N` elements with blocks of `B` threads you need $\lceil N/B \rceil$ blocks, written in integers as `(N + B - 1) / B`.

## Bounds check
Rounding up creates extra threads past the end of the data. Guard them:
```cuda
int i = blockIdx.x * blockDim.x + threadIdx.x;
if (i < n) { /* ... work on element i ... */ }
```
Without the guard those threads read and write memory they do not own.

**Worked example.** `N = 6`, block size 4. Grid = ⌈6/4⌉ = 2 blocks, 8 threads. Block 0 computes idx 0-3; block 1 computes idx 4, 5, 6, 7. Threads 6 and 7 fail `i < 6` and do nothing.

## 2D layouts for matrices
Row-major matrix of width `W`: element (row, col) sits at `row * W + col`. Map `x` to columns and `y` to rows:
```cuda
int col = blockIdx.x * blockDim.x + threadIdx.x;
int row = blockIdx.y * blockDim.y + threadIdx.y;
```
Putting `x` on the column axis matters for memory speed (chapter D1): consecutive `threadIdx.x` values then touch consecutive addresses.

## Limits
At most 1,024 threads per block (product of x, y, z). `gridDim.x` can be huge (up to 2³¹−1); `y` and `z` are limited to 65,535.

## Linearized thread id
Inside a block the hardware numbers threads in one line: `tid = threadIdx.x + threadIdx.y * blockDim.x + threadIdx.z * blockDim.x * blockDim.y`. This number, not the 2D coordinates, decides which warp a thread belongs to (chapter B3).

## 🎬 VIZ-INDEX-CALCULATOR: "Who am I?"
- *Canvas:* top: a row of block rectangles (blocks 0…G−1), each containing small thread squares. Bottom: a strip of the data array, one cell per element, aligned under the threads.
- *Controls:* number inputs **N**, **blockDim.x**, and a computed **gridDim.x**; a toggle **Show bounds check**; click any thread square to pin it.
- *Animation:* click a thread: a formula card appears: `idx = 1 × 4 + 2 = 6`, the numbers colour-matched to their sources (blockIdx purple, blockDim blue, threadIdx orange). A line drops from the thread to its element cell. If `idx ≥ N`, the line ends in a red ✖ "outside the array" and the thread is drawn hollow (idle).
- *Presets:* "N=6, block=4" (the worked example), "N=1000, block=256" (shows 24 idle tail threads).
- *Aha moment:* change **N** to a multiple of the block size and the idle threads disappear.
- *Accessibility:* "Thread 2 of block 1 maps to element 6, which is outside the array (N = 6); it does nothing."

## 🎬 VIZ-GRID-BUILDER: "Covering a matrix"
- *Canvas:* a matrix drawn as a grid of cells (up to 24×24 shown). Block tiles overlay it in alternating translucent colours, with block borders drawn thicker.
- *Controls:* **Matrix rows/cols**, **block shape** (drag the corner of a block, or choose 8×8, 16×16, 32×8, 32×32); toggle **x → col, y → row** versus **swapped**.
- *Animation:* hover a cell: its owning block and thread are highlighted, with the formulas for `row`, `col`, and `row*W+col` shown. Matrices that do not divide evenly show hatched out-of-range thread cells at the right and bottom edges.
- *Aha moment:* the swapped mapping is visibly legal but later (D1) shown to be slow.

## Check yourself
1. N = 1,000,000 and blockDim = 256. How many blocks?
2. Which element does thread 3 of block 5 handle when blockDim = 128?
3. Why can a kernel with no bounds check appear to work on some sizes and crash on others?

## Pitfalls
- Forgetting the bounds check.
- Integer division: `N / B` rounds down; use `(N + B - 1) / B`.
- Swapping row/col axes.

## Practice
[CU-001 Vector Addition](problem:CU-001) · [CU-002 Hadamard Product](problem:CU-002) · [CU-009 Matrix Addition](problem:CU-009) · [CU-010 Outer Product](problem:CU-010)

---

# CHAPTER B2: How blocks land on SMs
`id: B2 · part: B · est: 20 min · prereqs: A3, B1 · problems: CU-001 · pmpp: Ch. 4`

## Blocks are independent
The GigaThread Engine assigns each block to an SM and the block stays there until it finishes. Two rules follow, and you must design for both:
1. **No ordering.** Block 7 may run before block 0, or at the same time. Never assume order.
2. **No cooperation across blocks** within a kernel. Blocks cannot wait for each other. To combine results across blocks use atomics (E5) or a second kernel.

This independence is what lets the same program run on a 20-SM laptop GPU and a 132-SM data-center GPU: more SMs simply means more blocks at once.

## Residency
An SM holds several blocks at the same time, as many as its registers, shared memory and thread slots allow. All resident blocks' warps compete for the SM's schedulers. A block that is not resident waits in the queue.

## Waves and the tail effect
Suppose a GPU can hold 864 blocks at once (108 SMs × 8 blocks each, hypothetical). A grid of 1,000 blocks runs in two "waves": 864 in the first, only 136 in the second. In the second wave most SMs idle, so average utilization is 1000 / (2 × 864) ≈ **58%**. A grid of 1,728 blocks fills both waves perfectly. This **tail effect** is why a very small grid, or an awkward size, can underuse the machine. Grid-stride loops (D-chapters and plan §E1) are one fix.

## 🎬 VIZ-BLOCK-SCHEDULER: "Blocks find a home"
- *Canvas:* left, a queue of numbered block tokens. Centre: a grid of SM tiles, each drawn with 4-8 empty slots. Right: a utilization graph over time.
- *Controls:* **#SMs** (4-132), **blocks per SM**, **grid size** (blocks), **time per block** (uniform or random). **Play/Step**.
- *Animation:* tokens leave the queue and drop into free slots; when a block finishes (slot turns green and empties), the next token drops in. Tokens are numbered, and the finishing order is visibly *not* sorted.
- *Readouts:* wave count, overall utilization %, idle-SM time in the last wave.
- *Aha moment:* slide grid size from 864 to 1000 and utilization falls; slide to 1728 and it jumps back up. A toggle **Random block times** shows blocks completing out of order.

## Check yourself
1. Can block 3 read a value block 2 wrote earlier in the same kernel? Why not?
2. A grid has 100 blocks and the GPU can run 108 at once. What is wasted?
3. Why is "independent blocks" good for portability?

## Practice
[CU-001 Vector Addition](problem:CU-001): run with different block sizes and read the report.

---

# CHAPTER B3: Warps and lockstep
`id: B3 · part: B · est: 30 min · prereqs: B1, B2 · problems: CU-009, CU-018 · pmpp: Ch. 4`

## The warp is the real unit
The hardware does not schedule single threads. It cuts each block into **warps** of exactly **32 threads** and schedules warps. A warp's 32 lanes execute the same instruction in the same cycle. Everything about speed on a GPU (coalescing, divergence, bank conflicts) is a statement about *what the 32 lanes of one warp do together*.

## Linearized thread id → warp and lane
Take the linearized id from B1: `warp = tid / 32`, `lane = tid % 32`. For a 1D block of 256 threads that is 8 warps. For a 2D block the **x index varies fastest**, so:

| Block shape | Threads | Warps | What one warp holds |
|---|---|---|---|
| 256 × 1 | 256 | 8 | 32 consecutive x values of one row |
| 16 × 16 | 256 | 8 | **two** full rows (16 x-values × 2 y-values) |
| 8 × 8 | 64 | 2 | **four** rows of 8 |
| 33 × 1 | 33 | 2 | 32 threads + **one** thread (31 lanes idle) |

Block sizes that are not multiples of 32 waste lanes in the last warp.

## Scheduling and latency hiding
Each SM has four warp schedulers; each cycle each picks a **ready** warp and issues its next instruction. When a warp issues a global load it must wait hundreds of cycles for data. A CPU would stall; a GPU simply **switches to another resident warp**, at zero cost, because every warp's registers stay resident in the SM's register file. This is how the GPU hides memory latency: not with big caches, but by always having other work.

How many warps are "enough"? Use Little's law: data in flight = latency × bandwidth. On an A100, ~2 TB/s × ~400 ns ≈ 800 KB must be in flight across the chip *(approx.)*, about 7 KB per SM, which is roughly 58 warp-wide 128-byte loads outstanding per SM. That is why each SM wants many resident warps.

## 🎬 VIZ-WARP-FORMATION: "How a block is sliced into warps"
- *Canvas:* a 2D grid of thread squares (the block), up to 32×32. Threads are coloured by warp (8 repeating hues). Below it, the same threads laid out in a straight line in linearized order, with warp boundaries as thick vertical bars.
- *Controls:* **blockDim.x**, **blockDim.y** (number steppers), presets (256×1, 16×16, 8×8, 33×1, 32×4).
- *Animation:* hover a thread: its warp highlights in both views, and a tooltip shows `tid`, `warp`, `lane`. Partial warps are drawn with greyed-out empty lanes and a label "9 of 32 lanes used".
- *Readouts:* number of warps, **lane utilization %**.
- *Aha moment:* 8×8 puts four *rows* in a warp while 32×2 puts one row of 32; the second is what makes memory access contiguous (D1).

## 🎬 VIZ-LATENCY-HIDING: "Never wait"
- *Canvas:* a timeline: one row per warp (up to 16), time on x. Each warp's row is a sequence of coloured blocks: orange = issuing compute, blue = waiting on memory. At the bottom, a single "issue slot" row shows what the scheduler issues each cycle, and an "idle" count.
- *Controls:* **Resident warps** (1-32), **memory latency** (cycles), **compute per load** (instructions).
- *Animation:* with 1 warp the issue row is mostly empty (long blue gaps). Slide warps up: gaps fill, because each warp's wait overlaps with other warps' compute. A utilization meter climbs and plateaus.
- *Aha moment:* utilization saturates at a number of warps that depends on latency ÷ compute-per-load. Raise latency and more warps are needed to stay saturated.

## Check yourself
1. A block is 100 threads. How many warps, and how many lanes are wasted?
2. In a 16 × 16 block, which two rows share warp 0?
3. Why is switching between warps free?

## Pitfalls
- Block sizes that are not multiples of 32.
- Using tiny blocks (like 32) that leave too few warps resident per SM.

## Practice
[CU-009 Matrix Addition](problem:CU-009) · [CU-018 Mean and Variance](problem:CU-018)

---

# CHAPTER B4: Occupancy and resource limits
`id: B4 · part: B · est: 25 min · prereqs: B3 · problems: CU-040 · pmpp: Ch. 4, 6`

## What occupancy is
**Occupancy** = (resident warps on an SM) ÷ (maximum warps the SM supports). It measures how much latency-hiding capacity you have. More resident warps usually means better latency hiding, up to a point.

## Four limits; the smallest wins
Per SM *(approx., differs by architecture)*:

| Limit | T4 (Turing) | A100 (Ampere) |
|---|---|---|
| Max threads per SM | 1,024 | 2,048 |
| Max blocks per SM | 16 | 32 |
| Registers per SM | 65,536 | 65,536 |
| Shared memory per SM | up to 64 KB | up to 164 KB |

For your kernel, compute how many blocks fit under each limit; the minimum is the answer.

**Worked example.** Block = 256 threads, kernel uses 64 registers/thread, no shared memory.
- Registers per block = 256 × 64 = 16,384 → 65,536 / 16,384 = **4 blocks**.
- Thread limit: A100 2,048 / 256 = 8; T4 1,024 / 256 = 4.
- So A100: 4 blocks = 1,024 threads = 50% occupancy (**registers** are the limiter). T4: 4 blocks = 1,024 threads = 100% occupancy.

Same kernel, different occupancy on different chips.

## More is not always better
High occupancy hides latency, but a kernel that uses more registers per thread (to keep values close) can run faster at lower occupancy. Use occupancy as a diagnostic: if a memory-bound kernel runs at 12%, raise it; if it is already high, look elsewhere.

## Choosing a block size
Multiples of 32; 128 or 256 is a common starting point; check the occupancy limiter; try a few sizes and measure.

## 🎬 VIZ-OCCUPANCY-CALC: "What limits me?"
- *Canvas:* four horizontal bars (threads, blocks, registers, shared memory), each showing how much of the SM's budget the current configuration uses *per block*, stacked to show how many blocks fit. The tightest bar is outlined in red and labelled **limiter**. A big dial shows occupancy %.
- *Controls:* **Block size**, **registers/thread**, **shared memory/block**, **Profile** (T4 / A100).
- *Animation:* drag registers/thread from 32 up to 128; the register bar fills faster, the number of fitting blocks steps down (8 → 4 → 2), the dial falls in discrete jumps, and the limiter label switches from "threads" to "registers".
- *Aha moment:* the dial changes in *steps*, not smoothly, and the answer differs between T4 and A100.

## Check yourself
1. 128 threads/block, 32 regs/thread, 16 KB shared per block, A100 profile. Which limit binds?
2. Why can lowering registers per thread raise occupancy?
3. Name a case where lower occupancy can be faster.

## Practice
[CU-040 Block-Size Sweep](problem:CU-040)

---

# CHAPTER B5: The host side
`id: B5 · part: B · est: 20 min · prereqs: A2 · problems: CU-001 · pmpp: Ch. 2`

## The standard flow
```cuda
float *d_x;
cudaMalloc(&d_x, n * sizeof(float));                      // 1. allocate on device
cudaMemcpy(d_x, h_x, n * sizeof(float), cudaMemcpyHostToDevice);  // 2. copy in
kernel<<<grid, block>>>(d_x, /* ... */, n);               // 3. launch (async)
cudaMemcpy(h_y, d_y, n * sizeof(float), cudaMemcpyDeviceToHost);  // 4. copy out (waits)
cudaFree(d_x);                                            // 5. release
```
A plain `cudaMemcpy` waits for earlier GPU work to finish, which is why the result is ready when it returns. `cudaDeviceSynchronize()` waits explicitly.

## Errors
Launches do not return errors directly. After a launch call `cudaGetLastError()`; after synchronizing, check the return codes. In this course the simulator reports out-of-bounds accesses, double frees and leaks with the exact kernel, block and thread.

## Memory discipline
Every `cudaMalloc` needs a `cudaFree`. Leaked device memory is reported in the run report.

## 🎬 VIZ-HOST-TIMELINE: "Who is waiting for whom?"
- *Canvas:* two timeline lanes: **Host** (top) and **Device** (bottom), time on x.
- *Controls:* toggles **Insert cudaDeviceSynchronize after launch**, **Use blocking cudaMemcpy**, number of launches (1-4).
- *Animation:* the host lane issues tiny "launch" ticks immediately and moves on; the device lane shows kernel bars running after a small gap. Without sync, a host `printf` of the result appears *before* the kernel bar ends and is marked red "reads stale data". With sync, the host lane shows a hatched "waiting" bar until the kernel ends.
- *Aha moment:* launches are cheap and asynchronous; the host only waits when you tell it to (or when you do a blocking copy).

## Check yourself
1. After a kernel launch returns, is the output buffer ready?
2. What happens if you forget `cudaFree` in a loop of 1,000 iterations?

## Practice
[CU-001 Vector Addition](problem:CU-001)

---

# CHAPTER C1: Warp divergence
`id: C1 · part: C · est: 35 min · prereqs: B3 · problems: CU-003, CU-004, CU-016, CU-044 · pmpp: Ch. 4, 6`

## The problem
All 32 lanes of a warp share one instruction stream. What if the code says "if this lane's value is positive do A, otherwise do B" and the lanes disagree? The hardware cannot run A and B at the same time for different lanes. It runs **both paths one after the other**, with the lanes that do not belong to a path **masked off** (they sit idle), then the warp **reconverges** and continues together. That serialization is **warp divergence**.

```
warp:  lanes 0-31 reach  if (x > 0)  A  else  B
pass 1: run A   active mask = lanes where x > 0
pass 2: run B   active mask = lanes where x <= 0
then:   reconverge, all 32 lanes continue
time = time(A) + time(B)        (instead of max)
```

## What diverges and what does not
Divergence only happens **inside a warp**. A branch whose outcome is the same for all 32 lanes costs nothing extra.

| Condition | Diverges? | Why |
|---|---|---|
| `if (blockIdx.x % 2)` | no | all lanes of a block agree |
| `if (threadIdx.x / 32 == 0)` | no | the condition is constant within each warp |
| `if (threadIdx.x < 16)` | **yes** (warp 0) | lanes 0-15 and 16-31 disagree |
| `if (data[i] > 0)` | **depends on data** | random signs split most warps |

Worst cases: a `switch` with 32 different outcomes serializes up to 32 paths. A loop whose trip count differs per lane keeps the whole warp running for the *largest* trip count (lanes that finish early idle).

## Predication: when the compiler removes the branch
For a short conditional, the compiler may not emit a real branch at all. It computes with a per-lane **predicate** or uses a **select** instruction, so every lane executes the same instructions. A source-level `if` therefore *may* diverge, *may* be predicated. You cannot tell from the source alone. This is why we call the branch-free forms a **hazard removal**, not a guaranteed speed-up.

## Branchless vs divergence
For ReLU there are two ways to write the same function:

```cuda
// branchy form: compiler may or may not emit a divergent branch
if (in[i] > 0.0f) out[i] = in[i]; else out[i] = 0.0f;

// branchless form: one max instruction, every lane runs it, nothing to mask
out[i] = fmaxf(in[i], 0.0f);
```
The branchless form removes the question entirely. It also defines how `-0.0` and NaN behave through `fmaxf`'s documented rules, whereas an ad-hoc comparison may not. Other branch-free idioms: the ternary select `x > 0 ? x : 0`, clamping with `fminf/fmaxf`, and arithmetic masks (use with care around NaN and Inf).

Even for a **memory-bound** kernel such as ReLU, the branch-free form is the right idiom: it costs nothing and removes a hazard. (Chapter D2 shows why ReLU is memory-bound.)

## Volta and later: independent thread scheduling
Since Volta, each thread has its own program counter, so lanes can interleave in more ways and the hardware does not *promise* implicit reconvergence at a fixed point. When you need lanes to be in sync (before a warp shuffle, for example) say so explicitly with `__syncwarp()` or the `_sync` intrinsics (chapter F1).

## 🎬 VIZ-DIVERGENCE-LANES: "Both roads, one after the other"
- *Canvas:* top: a row of 32 `LaneStrip` squares with each lane's input value printed beneath (e.g., `-3, 2, -1, 5, …`). Middle: two "code panels" side by side, **Path A** (`out = x`) and **Path B** (`out = 0`). Bottom: a cycle timeline with a ruler, and a bar **"cycles used" vs "cycles if no divergence"**.
- *Controls:* **Data pattern** (all positive, all negative, alternating, random 50/50, first 16 positive), **Code form** toggle (**branchy** / **branchless fmaxf**), `Stepper`.
- *Animation (branchy):* step 1, the 32 lanes evaluate the condition; step 2, lanes that chose A flash orange while lanes for B go hollow-hatched; the Path A panel highlights. Step 3, the roles swap. Step 4, all lanes return to filled and a "reconverge" marker appears. The timeline shows two segments. *Animation (branchless):* one segment, all 32 lanes filled throughout.
- *Readouts:* **active lanes per step**, **warp efficiency %** (average active lanes ÷ 32), cycles used.
- *Aha moment:* with *all positive* data the branchy form runs only one path (no cost), with *alternating* data it runs both; the branchless form never changes. A small note appears: "The compiler may turn the branchy form into predicated code. This model shows the divergent case."
- *Accessibility:* "Pass 1 of 2: lanes 1, 3, 5… active (16 of 32). Pass 2 of 2: lanes 0, 2, 4… active."

## Check yourself
1. In a 256-thread block, does `if (threadIdx.x >= 128)` diverge? Which warps?
2. Each lane loops `tid % 8` times. How long does the warp's loop run?
3. Why can you not say "this `if` always diverges"?

## Pitfalls
- Branching on data when an arithmetic or intrinsic form exists.
- Arranging data so that neighbouring lanes take different paths when a reordering could make whole warps agree.

## Practice
[CU-003 ReLU](problem:CU-003) · [CU-004 Leaky ReLU](problem:CU-004) · [CU-016 Argmax](problem:CU-016) · [CU-044 Bitonic Sort](problem:CU-044)

---

# CHAPTER C2: Barriers and divergent barriers
`id: C2 · part: C · est: 25 min · prereqs: C1 · problems: CU-048, CU-050 · pmpp: Ch. 5`

## What `__syncthreads()` guarantees
It is a **block-wide barrier**: no thread continues past it until every thread of the block has reached it, and all shared-memory writes made before it are visible to the whole block after it. It is the tool for turning "each thread wrote its piece" into "everyone can read all pieces".

```cuda
tile[t] = global_data[i];   // each thread writes one slot
__syncthreads();            // wait until all slots are written
use(tile[(t + 1) % B]);     // now reading a neighbour's slot is safe
```

## The race it prevents
Without the barrier thread *t* may read slot *t+1* before thread *t+1* has written it. Three hazard names:
- **RAW** (read-after-write): read too early.
- **WAR** (write-after-read): overwrite a slot someone has not read yet. This is why tiled loops have a *second* barrier before loading the next tile.
- **WAW** (write-after-write): two threads write one slot with no order.

## The divergent barrier bug
Every thread of the block must reach the same `__syncthreads()`. If it sits inside an `if` that only some threads enter, the others never arrive. The behaviour is undefined: on hardware it can hang the kernel; in the simulator it is reported as a divergent-barrier diagnostic.

```cuda
if (idx < n) {            // BUG: threads with idx >= n skip the barrier
    tile[t] = in[idx];
    __syncthreads();
}
```
The fix is structural: keep *all* threads alive, **guard the loads and stores, not the barrier**.
```cuda
tile[t] = (idx < n) ? in[idx] : 0.0f;   // every thread participates
__syncthreads();
```
An early `return` for out-of-range threads before a barrier is the same bug in disguise.

## 🎬 VIZ-BARRIER-EPOCHS: "Who is waiting at the fence?"
- *Canvas:* a timeline with one horizontal track per thread (8 shown), time on x. Vertical dashed lines mark `__syncthreads()` barriers dividing time into **epochs**. Above: a strip of 8 shared-memory slots.
- *Controls:* a code panel with checkboxes to **remove barrier #1**, **remove barrier #2**, and a toggle **Put the barrier inside `if (t < 4)`**; `Stepper`; **Speed** randomization toggle (threads progress at different speeds).
- *Animation:* threads advance at different speeds. At a barrier, the early ones stop and show a "waiting" hatch; when the slowest arrives, all release together. When barrier #1 is removed, a read arrow from thread 3 hits slot 4 before thread 4's write arrives: the slot flashes red "RAW race: read before write" with the thread ids. With the barrier in `if (t < 4)`, threads 4-7 never arrive; the four waiting tracks stay hatched and a banner says "DEADLOCK: 4 threads never reached the barrier".
- *Aha moment:* races depend on timing, so they can pass 99 runs and fail on the 100th; the viz forces the bad schedule so you see it.

## Check yourself
1. Why does the tiled matmul loop need a barrier both after loading *and* before loading the next tile?
2. Can `__syncthreads()` synchronize two different blocks?
3. Rewrite the buggy snippet above so out-of-range threads still reach the barrier.

## Practice
[CU-048 Bug Hunt: Shared-Memory Race](problem:CU-048) · [CU-050 Bug Hunt: Divergent Barrier](problem:CU-050)

---

# CHAPTER D1: Global memory coalescing
`id: D1 · part: D · est: 30 min · prereqs: A4, B3 · problems: CU-009, CU-030 · pmpp: Ch. 6`

## How a warp's loads become transactions
When a warp executes a load, the hardware looks at the 32 addresses and merges them into as few **memory transactions** as it can. DRAM is read in chunks (32-byte *sectors*, grouped into 128-byte cache lines). If the 32 lanes read 32 consecutive floats, that is exactly 128 contiguous bytes: **one** line, four sectors, no waste. If the lanes read scattered addresses, the hardware fetches a whole sector for each lane, and most of those bytes are thrown away.

Define **efficiency** = useful bytes ÷ bytes actually moved.

| Access pattern (floats, 4 B) | Bytes moved per warp | Useful | Efficiency |
|---|---|---|---|
| `in[i]` stride 1, aligned | 128 | 128 | 100% |
| `in[i + 1]` stride 1, misaligned by one element | 160 (5 sectors) | 128 | 80% |
| `in[2*i]` stride 2 | 256 | 128 | 50% |
| `in[32*i]` stride 32 | 1,024 (32 sectors) | 128 | 12.5% |
| struct `{x,y,z}` array-of-structs, read only `.x` (12 B stride) | ~384 | 128 | ~33% |

## Rule of thumb
**Neighbouring threads should touch neighbouring addresses.** In a 2D kernel that means `threadIdx.x` should index the contiguous (column) axis of a row-major array. Swap them and every warp reads a strided column.

## AoS vs SoA
An array of structs interleaves fields in memory; reading one field strides across them. A **struct of arrays** keeps each field contiguous, so a warp reading `x[i]` is perfectly coalesced. Prefer SoA for GPU data.

## Coalescing is why layouts matter
Matrix transpose is the textbook case. If reads are coalesced then writes to the transposed layout are strided (or the reverse). The fix uses shared memory as a staging buffer (chapters D4 and D5).

## 🎬 VIZ-COALESCING: "From 32 addresses to transactions"
- *Canvas:* top: a `LaneStrip` of 32 lanes, each lane with an arrow pointing down to a memory strip. The memory strip is drawn as a long row of cells (4 bytes each) grouped into 32-byte sectors (alternating tint) and 128-byte lines (bold dividers).
- *Controls:* **Stride** slider (1, 2, 4, 8, 32), **Offset** slider (0-31 elements), **Element size** (4 B float / 16 B float4), **Layout preset** (contiguous, AoS 12-byte struct, column of a row-major matrix).
- *Animation:* press **Issue load**: the 32 arrows land; every sector that contains at least one requested byte lights up orange; requested bytes inside lit sectors are bright, unrequested bytes are dim. A counter ticks up the number of sectors fetched.
- *Readouts:* **transactions (sectors) = 4**, **bytes moved = 128**, **bytes useful = 128**, **efficiency = 100%**, with the numbers recomputing live.
- *Aha moment:* drag the offset from 0 to 1 and efficiency drops from 100% to 80%; drag the stride to 32 and it collapses to 12.5%, with a mountain of dim bytes.
- *Accessibility:* "Stride 2: 8 sectors fetched, 128 of 256 bytes useful (50%)."

## Check yourself
1. A kernel reads `in[threadIdx.x * 16]` (floats). Efficiency?
2. Why does swapping `x` and `y` in a 2D kernel make it slower even though the result is identical?
3. Why does AoS hurt when you only read one field?

## Pitfalls
- Column-wise access in a row-major array.
- Misaligned base pointers (rare with `cudaMalloc`, common with offset sub-arrays).

## Practice
[CU-009 Matrix Addition](problem:CU-009) · [CU-030 Matrix Transpose](problem:CU-030)

---

# CHAPTER D2: Roofline: memory-bound or compute-bound
`id: D2 · part: D · est: 30 min · prereqs: D1 · problems: CU-003, CU-005, CU-031 · pmpp: Ch. 6`

## Arithmetic intensity
**Arithmetic intensity** (AI) = floating-point operations ÷ bytes moved to and from global memory. It tells you whether a kernel is limited by arithmetic or by memory.

- ReLU: 1 compare-select per element, 4 B read + 4 B written = 8 B → **0.125 FLOP/byte**.
- Vector add: 1 FLOP, 12 B → 0.083. SAXPY: 2 FLOPs, 12 B → 0.167.
- Naive matrix multiply: each output needs 2K FLOPs and 2K loaded floats (8K bytes) → 0.25. With tiles of size T it becomes about T/4 (4 at T = 16, 8 at T = 32). Ideal large square matmul: N/6.

## The roofline
Attainable performance = min( peak compute, AI × peak bandwidth ). The point where the two meet is the **ridge point** = peak FLOPs ÷ peak bandwidth.

| GPU *(spec)* | Peak FP32 | Bandwidth | Ridge (FLOP/byte) |
|---|---|---|---|
| T4 | ~8.1 TFLOPS | 320 GB/s | ~25 |
| A100 | ~19.5 TFLOPS | ~2,039 GB/s | ~9.6 |
| H100 SXM | ~67 TFLOPS | ~3,350 GB/s | ~20 |

A kernel with AI below the ridge is **memory-bound**: runtime ≈ bytes ÷ bandwidth, arithmetic is nearly free. Above it, **compute-bound**.

ReLU at 0.125 versus a ridge of roughly 10-25 sits about two orders of magnitude to the left of the ridge. Its arithmetic units idle almost all the time, waiting for DRAM.

## What the classification tells you to do
- **Memory-bound** (maps, norms, softmax): the only levers are fewer bytes moved, coalesced access, enough warps in flight, and wider loads (D3). "Cleverer math" is pointless.
- **Compute-bound** (large matmul, with reuse): raise reuse (tiling, register blocking), keep the arithmetic pipelines full, avoid divergence.

Runtime for a memory-bound map ≈ **bytes ÷ achievable bandwidth**. For ReLU that is 8N ÷ BW.

## Arithmetic intensity as a diagnosis tool
Before optimizing, compute the kernel's AI and place it on the roofline. If you are already at the memory ceiling, no further tuning helps; stop.

## 🎬 VIZ-ROOFLINE: "Where does my kernel live?"
- *Canvas:* a log-log plot. x: arithmetic intensity (FLOP/byte, 0.01 → 1000). y: performance (GFLOP/s). A sloped line (memory roof) meets a flat line (compute roof) at the ridge point, which is labelled. Kernels are dots with names.
- *Controls:* **Profile** (T4 / A100 / H100 / RTX 4090), checkboxes for preset kernels (vector add, ReLU, SAXPY, softmax, naive matmul, tiled matmul T=16/32), **drag handle** to create a custom kernel by AI, and **Show my last run** (reads counters from the problem workspace).
- *Animation:* switching profile slides the ridge point left or right; tiling a matmul (T = 1 → 32) makes the dot climb diagonally up the memory roof toward the ridge. A shaded region left of the ridge is labelled **memory-bound**, right of it **compute-bound**.
- *Readouts:* for the selected dot: AI, attainable GFLOP/s, **% of roof**, bound classification, estimated time (from the model).
- *Aha moment:* ReLU sits far left of the ridge on every GPU; moving to a faster-arithmetic GPU does nothing for it, but moving to higher bandwidth does.
- *Accessibility:* "ReLU: 0.125 FLOP/byte, memory-bound. Ridge on A100 is 9.6."

## Check yourself
1. Compute AI of `y[i] = a * x[i] + y[i]` (4-byte floats).
2. Why does tiling a matmul raise AI?
3. A kernel is memory-bound. Does a faster `expf` help?

## Pitfalls
- Counting only the loads, forgetting the stores.
- Quoting AI with data that actually comes from cache (the roofline uses DRAM bytes).

## Practice
[CU-003 ReLU](problem:CU-003) · [CU-005 Sigmoid](problem:CU-005) · [CU-031 Matrix Multiplication](problem:CU-031)

---

# CHAPTER D3: float vs float4 (vectorized access)
`id: D3 · part: D · est: 25 min · prereqs: D1, D2 · problems: CU-012 · pmpp: Ch. 6`

## The idea
A normal load moves 4 bytes per thread. CUDA also has 8-byte (`float2`) and **16-byte** (`float4`) vector types. A single `float4` load or store moves 16 bytes in one instruction. For a bandwidth-bound kernel this gives:
- **fewer instructions** to issue for the same number of bytes;
- **more bytes in flight per thread**, which helps the memory system reach its ceiling with fewer warps.

```cuda
const float4* in4  = reinterpret_cast<const float4*>(in);
float4*       out4 = reinterpret_cast<float4*>(out);
float4 v = in4[i];            // one 16-byte load
/* ... apply the op to v.x, v.y, v.z, v.w ... */
out4[i] = v;                  // one 16-byte store
```

## Conditions
- **Alignment:** the address must be a multiple of 16 bytes. `cudaMalloc` returns well-aligned pointers; a sub-array starting at an odd offset is not.
- **Length:** `N` should be a multiple of 4. Handle the remaining 1-3 elements (the **tail**) with scalar code.
- **Grid size shrinks:** each thread handles 4 elements, so you need N/4 threads.

## When it helps, when it does not
It helps memory-bound maps that are already coalesced: you approach the bandwidth ceiling with fewer instructions. The gain varies by GPU and array size and is often modest; it does nothing for compute-bound kernels. **Always measure.** This course shows both a simulated curve and a curve measured on a real T4 (from a Colab run), clearly labelled which is which.

## 🎬 VIZ-FLOAT4-BANDWIDTH: "Does wider help?"
- *Canvas:* top: a line chart. x: array size (log, 1 KB → 1 GB); y: effective bandwidth (GB/s). Three lines: `float`, `float2`, `float4`. A dashed horizontal line marks the GPU's peak bandwidth. Bottom: a schematic of one warp issuing `float` (32 × 4 B) next to one issuing `float4` (32 × 16 B), with the instruction counts beside them.
- *Controls:* **Source toggle**: *Measured on T4 (Colab)* / *Simulator model*; **Alignment** toggle (aligned / offset by 4 B, which shows the fallback); **Operation** (copy, ReLU, SAXPY).
- *Animation:* switching source redraws the lines; the "measured" source shows a provenance badge (GPU name, CUDA version, date, median of N runs) and error bars. The warp schematic animates a load as 1 wide block vs 4 thin ones.
- *Aha moment:* small arrays are launch-dominated (lines overlap); large arrays separate the lines near the bandwidth ceiling; misalignment makes the float4 line lose its advantage.
- *Data note for the agent:* the "measured" series is a static JSON committed from the Colab notebook; the viz must never imply that simulator timings are T4 measurements.
- *Accessibility:* a table view of the plotted numbers.

## Check yourself
1. Why can a `float4` load fault if the pointer is offset by 4 bytes?
2. N = 1,000,003. How many `float4` elements and how many tail elements?
3. Would `float4` help a kernel that is compute-bound?

## Practice
[CU-012 ReLU with float4](problem:CU-012)

---

# CHAPTER D4: Shared memory and tiling
`id: D4 · part: D · est: 40 min · prereqs: C2, D1 · problems: CU-031, CU-032 · pmpp: Ch. 5`

## Shared memory is a scratchpad you control
Shared memory sits on the SM, is about as fast as the L1 cache, and is **managed by you**: you decide what to stage into it and when. It exists to **amortize repeated loads**: load a value from slow global memory *once*, then let many threads read it from fast shared memory.

**When not to use it.** A pure map (ReLU, vector add) loads each element exactly once. There is nothing to reuse, so shared memory only adds a copy and a barrier. Use it when data is read more than once.

## The tiling pattern
Take matrix multiply `C = A × B`. In the naive kernel each thread computes one output and reads a row of A and a column of B from global memory; neighbouring threads re-read the same rows and columns. In the tiled kernel a block cooperatively loads one `T × T` tile of A and one of B into shared memory, **synchronizes**, every thread uses the tiles for T multiply-adds, **synchronizes again**, and moves to the next tile along K.

```cuda
__shared__ float As[T][T], Bs[T][T];
float acc = 0.0f;
for (int t = 0; t < numTiles; ++t) {
    /* each thread loads ONE element of an A tile and ONE of a B tile
       (guard against out-of-range) */
    __syncthreads();                 // tiles fully loaded
    /* T multiply-adds from shared memory */
    __syncthreads();                 // everyone done before tiles are overwritten
}
/* write acc to C (guarded) */
```

## What you save
Each element of A and B is loaded from global memory once per tile instead of once per output. Global traffic drops by a factor of **T** (T = 16: 16× fewer loads). Shared memory use is 2·T²·4 bytes: 2 KB for T = 16, 8 KB for T = 32. Bigger tiles save more but consume more shared memory (lowering occupancy, B4) and registers.

## Edge tiles
When the matrix size is not a multiple of T, the last tiles hang over the edge. Load zeros for out-of-range elements and still reach both barriers (C2).

## 🎬 VIZ-TILING-STEPPER: "Load once, use many times"
- *Canvas:* three matrices drawn as grids: **A** (left), **B** (top), **C** (bottom right). A coloured T×T tile outlines the active block's output region in C, a matching horizontal strip in A and vertical strip in B. A "shared memory" panel below shows two small T×T slabs `As`, `Bs`.
- *Controls:* **Matrix size** (e.g., 8×8 to 32×32), **Tile size T** (2, 4, 8, 16), **Mode**: *Naive* / *Tiled*; `Stepper`.
- *Animation (tiled):* step 1: the active tile of A and B light up and copy into the slabs (arrows from global cells to shared cells). Step 2: barrier flash. Step 3: T partial products accumulate into the C tile (cells darken a little each step). Step 4: barrier flash, then the next tile along K slides in. *(Naive mode:* every C cell draws its own full row/column of arrows.)
- *Readouts:* **global loads so far**, **loads if naive**, **reduction factor** (should equal T), **shared bytes used**.
- *Aha moment:* flip between modes and watch the global-load counter differ by exactly T.
- *Accessibility:* "Tile 2 of 4: loaded 32 values into shared memory; 256 multiply-adds done; global loads so far: 64 vs 512 naive."

## Check yourself
1. Why are there two `__syncthreads()` in the loop?
2. M = N = K = 1024, T = 16. How many global loads of A (and B) per output element, naive vs tiled?
3. Why is shared memory useless for ReLU?

## Pitfalls
- Missing the second barrier (WAR race).
- Putting a barrier inside a bounds-check `if`.
- Using a tile so large that occupancy collapses.

## Practice
[CU-031 Matrix Multiplication](problem:CU-031) · [CU-032 Tiled Matrix Multiplication](problem:CU-032)

---

# CHAPTER D5: Bank conflicts
`id: D5 · part: D · est: 25 min · prereqs: D4 · problems: CU-030 · pmpp: Ch. 5-6`

## Shared memory is built from 32 banks
Shared memory is split into **32 banks**, each 4 bytes wide. Consecutive 4-byte words go to consecutive banks: word *w* lives in bank `w % 32`. In one cycle each bank can serve **one** address.

- If the 32 lanes of a warp access 32 words in **32 different banks**, all are served in one cycle.
- If *n* lanes hit **different addresses in the same bank**, the access is split into *n* serialized steps: an **n-way bank conflict**.
- If several lanes read the **same address**, the value is broadcast: no conflict.

## The classic case: a column of a 32×32 tile
`float tile[32][32]` stores row *r* at words `r*32 … r*32+31`. Reading a **row** (`tile[r][lane]`) hits 32 different banks. Reading a **column** (`tile[lane][c]`) puts word `lane*32 + c` in bank `(lane*32 + c) % 32 = c` for every lane, so all 32 lanes hit the same bank: a **32-way conflict**, 32× slower.

## Padding
Declare `float tile[32][33]`. Now word `lane*33 + c` is in bank `(lane + c) % 32`: all 32 lanes land in different banks. One extra column of padding removes the conflict. This is why transposes use `[32][33]` tiles.

## Detecting conflicts
The simulator's **Memory banks** panel and the counters report conflict counts per access, naming the line of code. Zero conflicts is the target.

## 🎬 VIZ-BANK-GRID: "32 lanes, 32 banks"
- *Canvas:* left: a shared-memory array drawn as a matrix (rows × columns) with every cell labelled by its bank number (0-31) and tinted by bank. Right: 32 bank columns (vertical bars) and 32 lane squares along the top, with lines from each lane to its bank.
- *Controls:* **Access pattern** (row, column, stride *s*, broadcast), **Row padding** (0 or 1), **Tile width** (32), `Stepper`.
- *Animation:* press **Issue access**: lane lines fly to banks; banks with more than one request stack the requests vertically and turn red with a number "×k". The timeline underneath shows k sequential cycles instead of 1.
- *Readouts:* **max conflict degree**, **cycles**, **slowdown ×**.
- *Aha moment:* with the column pattern, toggle padding 0 → 1 and the 32-high red stack on one bank dissolves into a flat row of single requests; the bank labels in the matrix visibly shift per row.
- *Accessibility:* "Column access, no padding: all 32 lanes hit bank 5: 32-way conflict, 32 cycles."

## Check yourself
1. Stride-2 access on 32 lanes (`s[2*lane]`): conflict degree?
2. Why does broadcast (all lanes read one address) not conflict?
3. With `[32][33]`, which bank does `tile[4][7]` use?

## Practice
[CU-030 Matrix Transpose](problem:CU-030)

---

# CHAPTER D6: Registers, local memory, constant and read-only cache
`id: D6 · part: D · est: 20 min · prereqs: A4, D4 · problems: CU-026, CU-027 · pmpp: Ch. 5, 7`

## Registers
The fastest storage. Each thread can use up to 255 registers, but every register a thread uses is one fewer available to other threads on the SM, so heavy register use lowers occupancy (B4). If a thread needs more than the compiler can allot, values **spill** into **local memory**, which is actually global memory (cached), and the kernel slows down. You can steer the compiler with `__launch_bounds__(maxThreads)` or `-maxrregcount`.

## Local memory
Per-thread arrays with dynamic indexing, and spilled registers, live here. It is private, but it is as slow as global memory (aside from caching), so avoid big per-thread arrays.

## Constant memory
A 64 KB read-only region with a dedicated cache. It is ideal for small data that every thread reads: a convolution filter, a lookup table, kernel parameters. When **all lanes of a warp read the same address**, the value is broadcast in one step. If lanes read *different* constant addresses, the reads serialize, so do not use it for per-thread indexing into a big table.

## The read-only path
Marking inputs `const float* __restrict__` tells the compiler the data is not written through other pointers and aliasing is absent, so it can use the read-only cache path and schedule loads more aggressively.

## 🎬 VIZ-REGISTER-PRESSURE: "The register budget"
- *Canvas:* a stacked bar for one SM's 65,536 registers, split into per-thread slices; to the right, a column of warp tokens showing how many warps are resident, and a small box "spilled to local memory".
- *Controls:* **Registers per thread** slider (16 → 255), **Block size**, **Profile**.
- *Animation:* increasing registers per thread shrinks the number of warp tokens in discrete steps; past the compiler limit a red portion labelled *spill* appears, and a bar "extra memory traffic" grows.
- *Aha moment:* two kernels with the same arithmetic can differ in speed only because one spills.

## Check yourself
1. Where does a spilled register live?
2. Which memory suits a 5×5 convolution filter read by every thread?
3. Why might `__restrict__` change performance?

## Practice
[CU-026 1D Convolution](problem:CU-026) · [CU-027 2D Convolution](problem:CU-027)

---

# CHAPTER E1: Map: elementwise kernels
`id: E1 · part: E · est: 25 min · prereqs: B1, C1, D2 · problems: CU-001 … CU-012 · pmpp: Ch. 2`

## The simplest pattern
A **map** applies the same function independently to every element: `out[i] = f(in[i])`. Vector add, Hadamard product, every activation function (ReLU, Leaky ReLU, Sigmoid, Tanh, Swish, GELU), and Dropout are maps. In TrenTorch Module 02 you wrote these in NumPy; here one thread owns one element.

## Everything you need is in B1, C1, D1, D2
- Index with the global-index formula; guard with `if (i < n)`.
- Consecutive lanes touch consecutive elements: perfectly coalesced.
- No reuse, so no shared memory.
- Low arithmetic intensity, so **memory-bound**: runtime ≈ bytes ÷ bandwidth.

## Grid-stride loop
Instead of launching one thread per element, launch a fixed grid sized for the GPU and let each thread loop:
```cuda
for (int i = blockIdx.x * blockDim.x + threadIdx.x;
     i < n;
     i += blockDim.x * gridDim.x) { /* ... element i ... */ }
```
One launch configuration then handles any `n`, launch overhead is amortized, and the tail effect (B2) disappears. Consecutive lanes still access consecutive elements on every iteration.

## Activation functions: cost per element
| Function | Notes |
|---|---|
| ReLU, Leaky ReLU | one compare/select; branch-free forms (C1) |
| Sigmoid, Tanh, Swish | one `exp` (or `tanh`) per element; `__expf` is faster and less accurate than `expf` |
| GELU (exact) | uses `erff`; more arithmetic but still memory-bound at large `n` |

The fast intrinsics (`__expf`, `__sinf`) use the SFU and trade a few units in the last place for speed. In a memory-bound map the difference barely shows, so prefer the accurate versions unless the problem says otherwise.

## Randomness in a map (Dropout)
Each thread needs its own random number with no shared state. Use a **counter-based** generator: hash `(seed, element index)` into a pseudo-random value. It is deterministic for a given seed (so tests are reproducible) and needs no memory.

## 🎬 VIZ-MAP-FLOW: "One thread, one element"
- *Canvas:* three aligned layers: the **input array** (cells), the **thread layer** (small squares grouped into warp-coloured blocks), and the **output array**. Arrows drop from input cell → thread → output cell.
- *Controls:* **N**, **block size**, **Mode**: *one thread per element* / *grid-stride loop with fixed grid*, `Stepper`, function dropdown (ReLU, Sigmoid, GELU).
- *Animation:* in one-per-element mode all threads fire in a single wave and the idle tail threads appear hatched. In grid-stride mode a small number of threads sweep along the array in strides, each thread's visited cells lit in its own colour with a loop-counter badge.
- *Readouts:* **bytes moved = 8N**, **FLOPs**, **AI**, **bound**.
- *Aha moment:* both modes produce identical output with different thread counts.

## Check yourself
1. Why does a map kernel not need shared memory?
2. A grid-stride kernel launches 1,024 threads for n = 10,000. How many elements does thread 5 process?
3. Why is a counter-based RNG a good fit for GPUs?

## Practice
[CU-001](problem:CU-001) · [CU-002](problem:CU-002) · [CU-003 ReLU](problem:CU-003) · [CU-004](problem:CU-004) · [CU-005](problem:CU-005) · [CU-006](problem:CU-006) · [CU-007](problem:CU-007) · [CU-008](problem:CU-008) · [CU-009](problem:CU-009) · [CU-010](problem:CU-010) · [CU-011](problem:CU-011) · [CU-012](problem:CU-012)

---

# CHAPTER E2: Reduction
`id: E2 · part: E · est: 45 min · prereqs: C2, D4, D5 · problems: CU-013 … CU-021 · pmpp: Ch. 10`

## The problem
A **reduction** turns many values into one: sum, max, min, dot product, norm, mean. It is the backbone of layer norm, softmax, losses and attention. It cannot be a pure map because every output depends on all inputs. The trick is a **tree**: add pairs, then add the pair-sums, and so on. N values take $\lceil \log_2 N \rceil$ steps and N−1 additions in total.

## One block's tree
Each thread loads an element into shared memory, then the block halves the active range repeatedly:
```cuda
for (int s = blockDim.x / 2; s > 0; s >>= 1) {
    if (tid < s) sdata[tid] += sdata[tid + s];   // combine two partials
    __syncthreads();                              // finish this level before the next
}
```
After the loop, `sdata[0]` is the block's partial result. To combine blocks you need a second stage: either write one partial per block and launch a second kernel, or have thread 0 of each block do an `atomicAdd` into one global value.

## The optimization ladder
| Step | Idea | What it fixes |
|---|---|---|
| 1 | Interleaved addressing, `if (tid % (2*s) == 0)` | (baseline) divergent, many idle lanes |
| 2 | Strided index, `index = 2*s*tid` | removes divergence but causes shared-memory bank conflicts |
| 3 | **Sequential addressing** (the loop above) | no divergence within warps while `s ≥ 32`, no bank conflicts |
| 4 | **First add during load**: each thread loads two elements and adds them | halves idle threads in the first step |
| 5 | **Warp shuffle** for the last 32 elements (F1) | no shared memory and no barriers for the last 5 levels |
| 6 | **Grid-stride** accumulation per thread before the tree, then atomics or two-pass | handles any N with a modest grid |

## Floating-point is not associative
Different summation orders give slightly different float results. Compare with a **tolerance**, not exact equality, and expect GPU sums to differ in the last digits from a CPU loop.

## Identity elements
Pad out-of-range threads with the operation's identity: 0 for sum, −∞ for max, +∞ for min. Every thread must still reach the barriers (C2).

## Reductions with a payload
**Argmax** reduces (value, index) pairs; define a tie-breaking rule (for example, lowest index) so the result is deterministic. **Dot product** is a map (multiply) fused with a sum. **Mean/variance** use two sums or Welford's update (E3).

## 🎬 VIZ-REDUCTION-TREE: "Fold the array in half"
- *Canvas:* a binary tree drawn bottom-up from 16 input leaves to 1 root. Each node is a thread slot; at each level, active threads are filled orange, inactive ones hollow. A side panel shows the shared-memory array state at each step.
- *Controls:* **Variant** dropdown (1-6 from the ladder), **N** (16 or 32), `Stepper`, toggle **Show bank numbers**.
- *Animation:* step through levels. Variant 1: active threads are every 2nd, 4th, 8th lane, so within one warp half the lanes are masked from step one (visible divergence). Variant 3: active threads are always the *low* indices `0..s−1`, so whole warps are fully active or fully idle. Variant 2 shows red bank-conflict chips on the shared-memory strip. Variant 5 replaces the last 5 levels with arrows hopping between lanes inside one warp, with no barrier marks.
- *Readouts:* **steps**, **active lanes per step**, **warp efficiency %**, **bank conflicts**, **barriers**.
- *Aha moment:* all six variants give the same sum, but the lane-activity graph beneath the tree is wildly different.

## Check yourself
1. Why must every thread, even out-of-range ones, reach each `__syncthreads()`?
2. Why is `0` the wrong padding value for a max reduction over negative numbers?
3. Two correct reductions of the same data differ by 1e-7. Is one a bug?

## Pitfalls
- `atomicMax` on floats is not built in for all targets; plan a workaround.
- Using the reduction result in the same kernel before all blocks have finished (blocks cannot wait for each other).

## Practice
[CU-013 Sum](problem:CU-013) · [CU-014 Max](problem:CU-014) · [CU-015 Min](problem:CU-015) · [CU-016 Argmax](problem:CU-016) · [CU-017 Dot Product](problem:CU-017) · [CU-018 Mean and Variance](problem:CU-018) · [CU-019 L1 Norm](problem:CU-019) · [CU-020 L2 Norm](problem:CU-020) · [CU-021 Cosine Similarity](problem:CU-021)

---

# CHAPTER E3: Row-wise ops: softmax, normalization, loss
`id: E3 · part: E · est: 40 min · prereqs: E2 · problems: CU-022 … CU-025 · pmpp: Ch. 10, 16`

## Shape of the problem
Given a matrix of `rows × cols`, do the same reduction-then-map **independently for each row**. Natural mapping: **one block per row** (or one warp per row if rows are short). Threads in the block stride across the row, reduce, then stride across it again to write.

## Stable softmax
$\text{softmax}(x)_j = e^{x_j} / \sum_k e^{x_k}$ overflows for large $x$. Subtract the row max first; the result is identical but the exponent is never positive. Steps per row: (1) max-reduce, (2) sum of $e^{x - m}$, (3) divide. That reads the row three times.

## Online softmax: one pass
Keep a running max $m$ and running sum $d$. When a new value $x$ arrives:
$$m' = \max(m, x), \qquad d' = d \cdot e^{m - m'} + e^{x - m'}$$
Two partial states $(m_1, d_1)$ and $(m_2, d_2)$ merge with the same rule, so each thread keeps its own state and the block combines them with a reduction. This is the core trick behind fused attention (F3).

## LayerNorm and RMSNorm
- **LayerNorm:** subtract the row mean, divide by $\sqrt{\text{var} + \epsilon}$, then scale and shift.
- **RMSNorm:** divide by $\sqrt{\text{mean}(x^2) + \epsilon}$; no mean subtraction.
Compute the sums in one pass. The shortcut $\text{var} = E[x^2] - E[x]^2$ can lose precision when the mean is large; **Welford's** running update (or a two-pass method) is safer. `rsqrtf` gives $1/\sqrt{\cdot}$ cheaply.

## Cross-entropy
For logits $z$ and target class $t$: loss $= \log\sum_k e^{z_k} - z_t$. The log-sum-exp is a stable softmax denominator. Reduce per row, then optionally average across rows.

## Memory view
These kernels are memory-bound. The goal is to touch each row's data as few times as possible: three reads is the baseline, one (online) is the target. The optimality certificate counts bytes against that lower bound.

## 🎬 VIZ-ROWWISE-SOFTMAX: "One block per row"
- *Canvas:* a small matrix (4 rows × 16 cols). Row 1 is expanded below into a strip of 16 values assigned to 8 threads (two values each). Under the strip: three stacked stage panels *max → exp & sum → divide*.
- *Controls:* **Mode**: *3-pass stable* / *naive unstable* / *online 1-pass*; **Logit scale** slider (1 → 100); `Stepper`.
- *Animation:* in *naive unstable* mode with large logits, `exp` cells turn red with "inf" and the output row becomes NaN. In *3-pass* mode three sweeps of arrows scan the row. In *online* mode a single sweep carries a small (m, d) badge that updates; at the end threads merge their badges in a mini tree.
- *Readouts:* **passes over the row**, **bytes read**, max abs error vs a reference.
- *Aha moment:* slide the logit scale up and the unstable mode breaks while the other two stay identical.

## Check yourself
1. Why does subtracting the max not change the softmax result?
2. Merge (m=2, d=3) with (m=5, d=1). What are the new m and d?
3. When can $E[x^2]-E[x]^2$ be badly wrong?

## Practice
[CU-022 Softmax](problem:CU-022) · [CU-023 RMS Norm](problem:CU-023) · [CU-024 Layer Norm](problem:CU-024) · [CU-025 Cross-Entropy](problem:CU-025)

---

# CHAPTER E4: Stencils and convolution
`id: E4 · part: E · est: 35 min · prereqs: D4, D6 · problems: CU-026 … CU-029 · pmpp: Ch. 7-8`

## Neighbourhood operations
In a **stencil** or **convolution** each output depends on a neighbourhood of inputs. A 1D filter of width K reads K inputs per output; a 3×3 2D filter reads 9; a 3D 3×3×3 filter reads 27. Neighbouring outputs share most of their inputs, so there is real reuse to exploit.

## Boundary handling
Near the edges the neighbourhood falls outside the array. Decide the rule (zero padding, clamp, or "valid" convolution that only produces interior outputs) and guard every read.

## Tiling with a halo
A block that computes a `T`-wide output tile needs `T + K − 1` inputs: the tile plus a **halo** of `(K−1)/2` cells on each side. Load that region into shared memory once, synchronize, then every thread reads its K neighbours from shared memory.

Loads per output: without tiling = K; with tiling ≈ (T + K − 1) / T. For a 2D 3×3 filter with a 16×16 output tile the block loads 18 × 18 = 324 inputs for 256 outputs: 1.27 per output instead of 9, about **7× fewer** global loads.

## Constant memory for the filter
Every thread reads the same filter weights in the same order: a perfect fit for constant memory (D6), which broadcasts them.

## Pooling
Max pooling reduces each window to one value. When the stride equals the window size, windows do not overlap, so there is **no reuse** and tiling adds nothing: just make sure the reads are coalesced.

## Higher dimensions
3D convolution has the same structure; shared-memory tiles grow cubically, so tile sizes are small and the halo overhead is a larger fraction.

## 🎬 VIZ-HALO-TILE: "Tile plus a halo"
- *Canvas:* a 2D input grid (e.g., 20×20). A bright tile marks the output region of one block; a lighter frame around it marks the halo; a 3×3 (or K×K) window slides inside the tile.
- *Controls:* **Filter size K** (3, 5, 7), **Tile size T**, **Mode**: *No tiling* / *Tiled with halo*, **Boundary rule**.
- *Animation:* press **Load**: tile + halo cells fly into a shared-memory panel (counter shows loads). Then the filter window sweeps the tile with no more global arrows. In *No tiling* mode every window step re-draws K² global arrows.
- *Readouts:* **loads per output**, **total global loads**, **halo overhead %**.
- *Aha moment:* grow K and the halo overhead grows; shrink T and the halo dominates, so the win vanishes.

## Check yourself
1. 1D filter K = 5, output tile T = 128. How many input elements does a block load?
2. Why is constant memory a good home for filter weights?
3. Does tiling help a stride-2, 2×2 max pool? Why not?

## Practice
[CU-026 1D Convolution](problem:CU-026) · [CU-027 2D Convolution](problem:CU-027) · [CU-028 Max Pool 2D](problem:CU-028) · [CU-029 3D Convolution](problem:CU-029)

---

# CHAPTER E5: Histogram and atomics
`id: E5 · part: E · est: 25 min · prereqs: E2 · problems: CU-033 · pmpp: Ch. 9`

## The write-conflict problem
A histogram counts how many inputs fall in each bin. Many threads may increment the same bin at the same time. A plain `bins[b]++` is a read-modify-write: two threads can read the same old value and both write old+1, losing a count. An **atomic** (`atomicAdd`) performs the whole read-modify-write indivisibly, so the result is correct.

## Contention
Atomics on the same address serialize. If most inputs land in a few bins (skewed data), thousands of threads queue on those few addresses and the kernel crawls even though it is "correct".

## Privatization
Give each block its **own private histogram in shared memory**. Threads do atomics into shared memory (fast, contention limited to one block), then after a barrier the block merges its private copy into the global histogram with one atomic per bin. Global contention drops from (number of elements) to (number of blocks × number of bins).

```cuda
__shared__ unsigned int local[BINS];
/* zero local[] cooperatively; __syncthreads(); */
/* each thread: atomicAdd(&local[bin(x)], 1u) for its elements */
/* __syncthreads(); then merge local[] into global bins with atomicAdd */
```

## Coarsening and the bin count
Letting each thread process several elements reduces the number of threads and the merge overhead. Privatization needs the bin array to fit in shared memory; for huge bin counts, other strategies apply.

## 🎬 VIZ-ATOMIC-CONTENTION: "Everyone wants the same bin"
- *Canvas:* a row of bins (bars) on the right; a swarm of small thread dots on the left, each drawing an arrow to its input's bin. A queue forms in front of any bin with more than one arrow.
- *Controls:* **Number of bins** (4-256), **Data skew** slider (uniform → 90% in one bin), **Mode**: *global atomics* / *privatized in shared*, **Show lost updates** (demo with non-atomic increments).
- *Animation:* global mode: arrows pile onto a hot bin and the queue length number grows; time bar stretches. Privatized mode: each block's mini-histogram fills quickly, then a short merge phase sends one arrow per bin to the global bars.
- *Readouts:* **max queue depth**, **atomic ops on global memory**, **estimated time**.
- *Aha moment:* with uniform data both modes are fine; at 90% skew the global mode explodes while privatized barely changes.

## Check yourself
1. Why can a non-atomic `bins[b]++` lose counts?
2. How many global atomics does the privatized version perform if there are 64 blocks and 256 bins?
3. When would privatization not fit?

## Practice
[CU-033 Histogram](problem:CU-033)

---

# CHAPTER E6: Prefix sum (scan)
`id: E6 · part: E · est: 40 min · prereqs: E2, D5 · problems: CU-034 · pmpp: Ch. 11`

## Definition
An **inclusive scan** of `[a0, a1, a2, a3]` is `[a0, a0+a1, a0+a1+a2, a0+a1+a2+a3]`. An **exclusive scan** shifts that right and starts with the identity (0). Scan looks serial (each output depends on the previous) but can be done in logarithmic depth.

## Why scan matters
It computes *positions*. Stream compaction ("keep elements that pass a test") uses a scan of 0/1 flags to find each survivor's output slot. Radix sort (E8) is built from scans. Many "irregular" algorithms become regular once you have a scan.

## Hillis-Steele (simple, work-inefficient)
In step *k*, every element adds the value `2^k` positions to its left: log₂ N steps, but about N log₂ N additions. Simple and fast for one block. It needs double buffering (or careful ordering) so threads do not read values already updated in the same step.

## Blelloch (work-efficient)
Two sweeps over a tree:
- **Up-sweep (reduce):** build partial sums up the tree; the root holds the total.
- **Down-sweep:** set the root to 0 (identity), then push prefixes back down.
About 2(N−1) additions: **O(N) work** instead of O(N log N), but 2 log₂ N steps. Shared-memory accesses use power-of-two strides, which creates bank conflicts; padding the index fixes it (D5).

## Beyond one block
Scan each block, write each block's total, scan the block totals, then add each block's offset to its elements (three phases, or two kernels).

## 🎬 VIZ-SCAN-NETWORK: "Two ways to prefix-sum"
- *Canvas:* 8 columns (elements) and rows representing steps, drawn as a wiring diagram. Circles are adders; arrows show where each value comes from.
- *Controls:* **Algorithm** (Hillis-Steele / Blelloch), **Input** (editable 8 numbers), `Stepper`.
- *Animation:* Hillis-Steele: each row, every column (from offset onward) adds a partner at a growing distance; counts of adders per row stay near N. Blelloch: a shrinking up-sweep tree, a root-reset to 0 flashed, then an expanding down-sweep.
- *Readouts:* **steps (depth)**, **total additions (work)**, **result**.
- *Aha moment:* for N = 8 the totals show 17 vs 14 additions: the gap grows with N.
- *Accessibility:* a table view of each step's array.

## Check yourself
1. Inclusive vs exclusive scan of `[3, 1, 7, 0]`.
2. How does a scan of 0/1 flags give output positions for compaction?
3. Why does Hillis-Steele need a second buffer?

## Practice
[CU-034 Prefix Sum (Scan)](problem:CU-034)

---

# CHAPTER E7: The matrix multiplication ladder
`id: E7 · part: E · est: 60 min · prereqs: D2, D4, D5, E4 · problems: CU-031 … CU-037 · pmpp: Ch. 5-6`

## Why matmul
Linear layers, attention and convolutions (via im2col) all reduce to matrix multiplication. TrenTorch's `Linear` (Module 03) is a matmul plus bias. It is the best example of a kernel you can make dramatically faster by climbing a ladder of ideas, each fixing a measured bottleneck.

## Step by step
| Version | Idea | Global loads per output (K inner dim) | Notes |
|---|---|---|---|
| v1 Naive | one thread per output | 2K | AI ≈ 0.25 FLOP/byte (cache may help) |
| v2 Coalescing fix | map `threadIdx.x` to the **column** axis | 2K | same loads, far better transactions: threads in a warp read consecutive B elements and broadcast one A element |
| v3 Shared-memory tiles | tile size T | 2K / T | AI ≈ T/4; two barriers per tile |
| v4 Thread coarsening | each thread computes several outputs | lower still | more reuse from registers; fewer, fatter threads |
| v5 Vectorized loads | `float4` into shared memory | same | fewer load instructions (D3) |
| v6 Register tiling + padding | each thread holds a small 2D block of C in registers; pad shared tiles | much lower | bank-conflict-free, high AI, register pressure matters |
| v7 Double buffering *(concept)* | load the next tile while computing the current | same | hides load latency; asynchronous copy instructions on newer GPUs; **not simulated here** |

Tensor cores can deliver far more throughput still; they are out of scope for the simulator but you should know they exist.

## Reading the ladder on the roofline
Each version moves the kernel's point up and to the right (D2): fewer bytes per FLOP means higher AI, until you approach the compute roof or run into register/occupancy limits (B4). A well-optimized version reaches a large fraction of peak; do not expect to match a vendor library without tensor cores.

## What each rung costs
Tiling costs shared memory and barriers; coarsening costs registers; vectorizing costs alignment constraints; padding costs a little shared memory. The skill is knowing which bottleneck the *report* shows and choosing the matching rung.

## 🎬 VIZ-MATMUL-LADDER: "Climb the ladder"
- *Canvas:* a horizontal scrubber with seven stops (v1…v7). Above it, a panel for the selected version: the three matrices with one block's footprint outlined; arrows from global memory (thickness proportional to bytes). Below: a mini roofline with a dot per version and a bar chart of global loads, shared bytes, and estimated time.
- *Controls:* **Version scrubber**, **Matrix size** (e.g., 64/128/256), **Profile**; a **Run in simulator** button that fills the bars from real counters for versions the learner has solved.
- *Animation:* dragging the scrubber morphs the picture: v1 shows every thread pulling its own row/column (a forest of arrows); v3 shows tile-sized blue arrows into a shared slab; v4/v6 show each thread owning a small block of C; v7 shows two shared slabs alternating.
- *Readouts:* **global loads**, **shared-memory bytes**, **bank conflicts**, **AI**, **estimated time (modelled)**.
- *Aha moment:* the bars shrink at every step and the roofline dot climbs, with the "why" sentence under each stop.

## Check yourself
1. In v1, why do the 32 lanes of a warp reading `A[row][k]` not cost 32 loads?
2. What is the AI of tiled matmul with T = 32?
3. Name one downside of increasing the tile size.

## Practice
[CU-031](problem:CU-031) · [CU-032](problem:CU-032) · [CU-035 Coarsened](problem:CU-035) · [CU-036 Vectorized + bank-free](problem:CU-036) · [CU-037 Fused MatMul+Bias+ReLU](problem:CU-037)

---

# CHAPTER E8: Sorting day: why quicksort struggles on GPUs
`id: E8 · part: E · est: 40 min · prereqs: C1, E6 · problems: CU-044, CU-045 · pmpp: Ch. 12-13`

## Quicksort in one paragraph
Pick a pivot, partition the array into "less than" and "greater than", recurse on both halves. On a CPU, it is excellent. On a GPU it is awkward for three reasons.

1. **Data-dependent branching.** The core step asks `if (a[i] < pivot)` per element. Neighbouring lanes hold random values, so the branch splits warps (C1) and the partition runs at a fraction of full efficiency.
2. **Irregular, shrinking parallelism.** The recursion tree starts with one big partition (little parallelism to exploit at the first few levels) and ends with many tiny ones (too small to fill a warp). Sub-problems have wildly different sizes, so blocks finish at different times (B2 tail effect).
3. **Scatter writes.** Each element goes to a data-dependent position, which tends to break coalescing (D1).

GPU quicksorts exist and can be made to work, but they are rarely the fastest choice. The better answer is to pick an algorithm whose control flow does not depend on the data.

## Bitonic sort: a fixed network
A **sorting network** is a fixed schedule of compare-exchange operations: "compare elements *i* and *j*, put the smaller first". The schedule never looks at the data. Bitonic sort builds one for powers of two:
- Comparators per stage: N/2, all independent.
- Stages: log₂N · (log₂N + 1) / 2, so 55 stages for N = 1,024.
- Total work O(N log² N): more than quicksort's average, but perfectly regular.
Each compare-exchange can be written branch-free with `fminf`/`fmaxf` (or integer min/max), so **there is no divergence at all**.

## Radix sort: built from scan
For each digit (a few bits at a time): compute a flag per element, **scan** the flags to compute each element's destination, then scatter. Work is O(k · N) for k-bit keys, and the passes are stable. Libraries use radix sort for numeric keys because it maps so well onto scan (E6) and coalesced access. It is a great example of the "make irregular work regular with a scan" idea.

## Merge-based sorts
Sort small tiles in shared memory, then merge sorted runs in parallel using binary search to split the work evenly. Useful for comparison sorts of general types.

## Which to choose
| | Divergence | Work | Notes |
|---|---|---|---|
| Naive GPU quicksort | high | ~N log N | irregular, hard to balance |
| Bitonic | none | N log² N | simplest to write, power-of-two N |
| Radix | none | k · N | best for integer/float keys |
| Merge | low | N log N | general comparators |

## 🎬 VIZ-QUICKSORT-DIVERGENCE: "Partitioning a warp"
- *Canvas:* top: an array of 32 values assigned to 32 lanes, with a pivot value shown. Middle: the `LaneStrip` with active/masked states. Bottom: a **lane-utilization-over-time** graph and a small recursion tree whose nodes are sized by partition length.
- *Controls:* **Array shape** (random, sorted, many duplicates), **Algorithm** (quicksort / bitonic), `Stepper`.
- *Animation:* quicksort: lanes with value < pivot go "left" (orange), others masked, then roles swap; utilization hovers near 50%. The recursion tree grows lopsided for sorted input. Bitonic: a sweep of aligned compare-exchange arrows; all 32 lanes stay active in every stage.
- *Readouts:* **average lane utilization %**, **stages/steps**, **max recursion depth** (quicksort).
- *Aha moment:* sorted input makes the quicksort tree a long skinny chain (bad pivots), while bitonic does not care about the input at all.

## 🎬 VIZ-BITONIC-NETWORK: "A sort that never looks at the data"
- *Canvas:* a classic network diagram: 8 or 16 horizontal wires; vertical connectors are compare-exchange elements, arranged in stages. Arrows on each connector show the direction smaller values move.
- *Controls:* **N** (8 or 16), **Input** (editable), `Stepper`, toggle **Show stage number**.
- *Animation:* values travel along the wires; at each connector the pair swaps if out of order (the swap flashes). Stage counter ticks.
- *Readouts:* **stage**, **comparators executed**, **swaps made**.
- *Aha moment:* the wiring is identical for every input.

## Check yourself
1. Why can the same sorting network sort any input?
2. How many stages does bitonic sort need for N = 16?
3. How does a scan of flags give the destination slots in a radix-sort pass?

## Practice
[CU-044 Bitonic Sort](problem:CU-044) · [CU-045 Radix Sort](problem:CU-045)

---

# CHAPTER F1: Warp-level primitives
`id: F1 · part: F · est: 25 min · prereqs: B3, C1, E2 · problems: CU-046 · pmpp: Ch. 10, 22`

## Lanes can talk to each other directly
Within a warp, lanes can exchange register values **without shared memory and without a barrier**. These **warp shuffle** intrinsics take a mask of participating lanes (use `0xffffffff` for the full warp) and a value:
- `__shfl_down_sync(mask, v, delta)`: lane *i* gets lane *i+delta*'s value.
- `__shfl_xor_sync(mask, v, laneMask)`: butterfly exchange.
- `__shfl_sync(mask, v, srcLane)`: broadcast from one lane.
Voting: `__ballot_sync` returns a 32-bit mask of lanes where a predicate holds; `__any_sync`, `__all_sync`. `__syncwarp()` makes lanes reconverge.

## Warp reduction
```cuda
for (int off = 16; off > 0; off >>= 1)
    v += __shfl_down_sync(0xffffffff, v, off);
// lane 0 now holds the sum of all 32 lanes
```
Five steps, no shared memory, no barrier. A full block reduction then needs only one value per warp in shared memory.

## Why the `_sync` and the mask
Since independent thread scheduling (C1) lanes may not be converged. The mask names exactly which lanes must participate, and the call waits for them. Calling a shuffle with a lane missing from the mask but present in the warp is a bug.

## 🎬 VIZ-SHUFFLE-NETWORK: "Lanes passing notes"
- *Canvas:* 32 lanes in a row, each with a value; arcs show where each value is read from.
- *Controls:* **Intrinsic** (`shfl_down`, `shfl_xor`, `shfl` broadcast, `ballot`), **delta / mask** input, `Stepper`; a preset **Warp reduction** that runs offsets 16, 8, 4, 2, 1 in sequence.
- *Animation:* in a reduction step each lane's arc reaches `offset` lanes to the right; values add; lanes past the end get their own value back (greyed because they are not used). After five steps lane 0 shows the total, with the running partials faintly visible.
- *Aha moment:* the whole 32-lane sum finishes in five steps with no shared-memory slab in sight.

## Check yourself
1. What does lane 29 receive from `__shfl_down_sync(mask, v, 4)`?
2. Why is a full-warp mask required if all 32 lanes execute the call?
3. How would you reduce a 256-thread block using shuffles?

## Practice
[CU-046 Warp-Shuffle Reduction](problem:CU-046)

---

# CHAPTER F2: Streams and overlap
`id: F2 · part: F · est: 25 min · prereqs: A2, B5 · problems: theory + playground only · pmpp: Ch. 20, 22`

## The idea
A **stream** is an ordered queue of GPU work. Operations in one stream run in order; operations in different streams may overlap. Modern GPUs have separate engines for copies and for compute, so a copy for chunk *k+1* can run while the kernel for chunk *k* runs.

## Requirements
- Use **pinned (page-locked) host memory** (`cudaMallocHost`) so copies can be asynchronous.
- Use `cudaMemcpyAsync` with an explicit stream, and launch the kernel into that stream.
- Split the data into chunks, and give consecutive chunks different streams.

## What you gain
Without overlap the total is *copy-in + compute + copy-out*. With S chunks and overlap the total approaches the **longest** of the three plus a small pipeline fill/drain cost. If copying dominates (PCIe is slow, A2), overlap hides compute; if compute dominates it hides copies.

## Limits
More streams than needed add overhead. Overlap only helps when there is something to overlap (large enough work, independent chunks). The browser simulator may not model all stream behaviour, so this chapter is a model-driven visualization plus text.

## 🎬 VIZ-STREAM-TIMELINE: "Overlap copies and compute"
- *Canvas:* three horizontal lanes: **H2D engine**, **Compute**, **D2H engine**; time on x. Chunks appear as coloured rectangles.
- *Controls:* **Number of chunks/streams** (1-8), **copy time**, **compute time**, **pinned memory** toggle.
- *Animation:* with 1 stream the rectangles go strictly left to right in a staircase. With 4 streams the lanes fill diagonally and the total length shrinks; with pinned memory off, the H2D lane blocks and the overlap disappears.
- *Readouts:* **total time**, **speed-up vs 1 stream**, **bottleneck lane**.

## Check yourself
1. Why must host memory be pinned for async copies to overlap?
2. Copy = 40 ms, compute = 10 ms, 4 chunks. Roughly how long with perfect overlap?

---

# CHAPTER F3: Kernel fusion and attention
`id: F3 · part: F · est: 40 min · prereqs: D2, E3, E7 · problems: CU-037 (also CU-038, CU-039) · pmpp: Ch. 16, 22`

## Why fuse
Every kernel reads its inputs from global memory and writes its outputs back. For memory-bound steps that traffic **is** the cost. Chaining three elementwise kernels moves each intermediate to memory and back; one fused kernel does all three in registers and moves only the final result.

Example: `y = relu(x + bias)` unfused: kernel 1 reads x and bias, writes t (3 transfers of 4 B per element); kernel 2 reads t, writes y (2 transfers) = 20 B per element. Fused: read x, bias, write y = 12 B. About **40% less traffic**, so about 40% less time for a memory-bound step.

A **fused epilogue** applies bias and an activation to a matmul's accumulator while it is still in registers, before writing C once (CU-037).

## Attention, and the matrix you never write
Attention computes `softmax(Q Kᵀ / √d) V`. The score matrix `S = Q Kᵀ` is N × N. For N = 4,096 and 4-byte floats that is 64 MB per head, written, re-read for softmax, written again, and re-read for the `V` product. The **FlashAttention** idea removes that traffic:
- process Q in row blocks; for each, stream over K and V in tiles;
- compute a tile of scores, update a running **online softmax** state (E3) and a running output accumulator;
- never store S to global memory.
This uses everything from earlier chapters: tiling (D4), online softmax (E3), fusion.

## TrenTorch connection
Module 12 builds attention in NumPy; Module 17 (acceleration) is where a GPU backend would plug in. The mini-attention problem is a small version of this fusion.

## 🎬 VIZ-FUSION-TRAFFIC: "Count the round trips"
- *Canvas:* a pipeline diagram of 3-4 operations drawn as boxes. Between each pair: an arrow to and from a "global memory" bar at the bottom (unfused), versus arrows staying in a "registers" strip (fused).
- *Controls:* **Pipeline preset** (bias+ReLU, matmul+bias+GELU, scale+mask+softmax), **Fuse** toggle, **Tensor size**.
- *Animation:* toggling **Fuse** deletes the intermediate arrows with a satisfying collapse; a byte counter and a time bar shrink.
- *Readouts:* **bytes moved**, **estimated time**, **traffic saved %**.
- *Second panel (attention):* an N × N square scales with N; toggle **Flash-style tiling** to replace it with a small sliding tile and a running (m, d) badge; the memory number drops from O(N²) to O(N).

## Check yourself
1. Fused vs unfused traffic for `y = relu(a*x + b)` with three element-wise stages?
2. Why does materializing the N × N score matrix hurt at large N?
3. Which earlier chapter supplies the online-softmax trick?

## Practice
[CU-037 Fused MatMul + Bias + ReLU](problem:CU-037) · [CU-038 Fused Softmax](problem:CU-038) · [CU-039 Mini Attention](problem:CU-039)

---

# CHAPTER F4: Multi-GPU and NCCL
`id: F4 · part: F · est: 35 min · prereqs: A2, E2 · problems: CU-047, CU-051 · pmpp: Ch. 20`

## Why more than one GPU
Models and datasets outgrow one GPU, and training is faster in parallel. The standard scheme, **data parallelism**: each GPU holds a copy of the model, processes its own slice of the batch, computes gradients, and then **all GPUs average their gradients** so the copies stay identical. That average is a collective operation called **AllReduce**.

## NCCL and collectives
NCCL is the library for GPU collectives. Core operations: **AllReduce**, **Broadcast**, **AllGather**, **ReduceScatter**, **AllToAll**, point-to-point **Send/Recv**.

## Ring AllReduce
Arrange the *p* GPUs in a ring and split the data into *p* chunks.
1. **Reduce-scatter** (p−1 steps): each step every GPU sends one chunk to its neighbour and adds the chunk it receives, so each GPU ends up owning the full sum of one chunk.
2. **All-gather** (p−1 steps): the finished chunks travel around the ring until everyone has all of them.
Total steps 2(p−1). Each GPU sends about $2 \cdot \frac{p-1}{p} \cdot D$ bytes for data size D, which is nearly independent of *p*: the algorithm is **bandwidth-optimal** and scales well.

## Topology matters
A fast all-to-all fabric (NVLink + NVSwitch) vs a ring vs a PCIe tree through the host changes the effective bandwidth by a large factor (the simulator models these topologies).

## Deadlocks
Every rank must call the same collectives in the same order with matching sizes. If rank 3 skips a call, or calls `AllReduce` with a different count, the others wait forever. The simulator detects rank, count and ordering mismatches and reports the offending rank.

## 🎬 VIZ-RING-ALLREDUCE: "Pass it around the ring"
- *Canvas:* *p* GPU nodes on a circle, each holding a small bar chart of *p* chunks. Arrows between neighbours.
- *Controls:* **GPUs** (2-16), **Topology** (ring / NVSwitch mesh / PCIe tree), `Stepper`, **Data size**.
- *Animation:* phase 1 (reduce-scatter): coloured chunks hop one node per step and add into the receiver's matching chunk (the bar grows). Phase 2 (all-gather): finished chunks hop around until every node's chart is full. A bandwidth meter on each link shows load.
- *Readouts:* **steps = 2(p−1)**, **bytes per GPU**, **estimated time for this topology**.
- *Aha moment:* raise the GPU count and the steps go up but the bytes per GPU barely change.
- *Failure mode:* a **Skip rank** toggle shows one node refusing to participate and the others stalling with a red "waiting for rank 3".

## Check yourself
1. Why is each GPU's total traffic nearly constant as *p* grows?
2. What causes an NCCL deadlock from a mismatched call order?
3. Which collective is used to sum gradients across data-parallel replicas?

## Practice
[CU-047 Multi-GPU AllReduce](problem:CU-047) · [CU-051 Bug Hunt: NCCL Deadlock](problem:CU-051)

---

# CHAPTER F5: Debugging and the profiling mindset
`id: F5 · part: F · est: 30 min · prereqs: C2, D1, D5 · problems: CU-048, CU-049, CU-050, CU-051 · pmpp: Ch. 6, 22`

## A working method
1. **Correct first.** A fast wrong kernel is worthless. Test small, then edge sizes (N not a multiple of the block size, N < blockDim).
2. **Classify.** Compute AI and place the kernel on the roofline (D2). Memory-bound or compute-bound?
3. **Find the lever.** Memory-bound: bytes, coalescing, occupancy, vector width. Compute-bound: reuse, divergence, instruction mix.
4. **Change one thing, measure again.**
5. **Stop** when you reach the roof.

## The four classic bugs
| Bug | Symptom | Cause | Fix |
|---|---|---|---|
| Out-of-bounds | garbage, crash, intermittent | missing/incorrect bounds check | guard every access (B1) |
| Shared-memory race | wrong answers that change between runs | missing `__syncthreads()` (RAW/WAR/WAW) | add the barrier (C2) |
| Divergent barrier | hang | barrier inside a conditional | all threads reach it (C2) |
| Collective mismatch | multi-GPU hang | ranks disagree on call order/size | align calls (F4) |

## Reading a report
The simulator's report shows bytes moved at each level, FLOPs, bank conflicts, divergence, and bound classification. Read it top to bottom: (1) did it run clean? (2) how many bytes vs the lower bound? (3) any conflicts? (4) which side of the ridge?

## 🎬 Interactive (no dedicated viz): "Annotated report"
- A workspace example that displays a real report with numbered callouts (①-⑥) pointing to each field, plus a "What this tells you" side panel that changes as the learner hovers each callout. Reuse the Results panel components from the problem workspace.

## Check yourself
1. A kernel gives different results on repeated runs. Name two likely causes.
2. Your report says 1,024 bytes moved per 128 useful. What is the efficiency and which chapter helps?

## Practice
[CU-048](problem:CU-048) · [CU-049](problem:CU-049) · [CU-050](problem:CU-050) · [CU-051](problem:CU-051)

---

# CHAPTER F6: Capstone: a fused MLP block
`id: F6 · part: F · est: 90 min · prereqs: E7, F3 · problems: CU-052 · pmpp: Ch. 16, 19`

## The goal
Build the forward pass of a transformer-style MLP block on the GPU using kernels you wrote:
```
h = GELU(x · W1 + b1)       (matmul with a fused bias+GELU epilogue)
y = h · W2 + b2 + x         (matmul, bias and residual add)
```
and verify it against the NumPy `Linear` + activation you built in TrenTorch Modules 02 and 03.

## Milestones
1. **Correctness.** Tiled matmul (CU-032) and the activation (CU-008) work individually.
2. **Fusion #1.** Fuse bias + GELU into the first matmul's epilogue (CU-037 pattern).
3. **Fusion #2.** Fuse bias + residual into the second matmul.
4. **Account for bytes.** Use the report to compare your fused block against the unfused sequence; explain the difference with a bytes-moved table.
5. **Roofline.** Place each kernel on the roofline and say which are memory- and compute-bound.

## Bridge to TrenTorch
Module 17 (acceleration) is where the framework chooses a faster backend. The capstone is the proof of concept: the same math as Module 03/02, executed by kernels you wrote and measured.

## 🎬 VIZ-CAPSTONE-PIPELINE: "Your block, end to end"
- *Canvas:* a left-to-right dataflow diagram: `x → [matmul + bias + GELU] → h → [matmul + bias + residual] → y`. Under each node: the kernel the learner wrote (linked) and its live metrics.
- *Controls:* **Fusion level** (none / epilogue-fused), **Run all** (executes the learner's kernels in sequence in the simulator).
- *Animation:* data tokens flow through the nodes; a memory-traffic strip below swells at each global-memory write; fusion visibly deletes the intermediate write.
- *Readouts:* **total bytes**, **per-kernel bound**, **end-to-end max error vs NumPy reference**.

## Check yourself
1. How many global writes of the intermediate `h` does the fused version avoid?
2. Which kernel in this block is more likely compute-bound, and why?

## Practice
[CU-052 Capstone: Fused MLP Block](problem:CU-052)

---
