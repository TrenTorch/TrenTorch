# TrenTorch CUDA Section: Master Build Plan

> **Audience:** the coding agent that will build this section.
> **Read order:** §0 (rules and unknowns) → §1 (architecture) → §2 (content model) → §3–§6 (course content) → §7–§8 (system design) → §9 (roadmap and acceptance criteria).
> Every section ends in something checkable. Do not skip Phase 0.

---

## 0. Context, rules and things to verify first

### 0.1 What we are building
A **CUDA** section for TrenTorch (live site **https://trentorch.com**, framework repo `TrenTorch/TrenTorch`). The site already has an in-browser IDE at `/ide/<slug>` (tabs Description / Hints / Solution / Discussion, panels Guide / Editor / Output, Run + Submit, a language dropdown, hidden tests), a problemset, 12 topic modules, a DSA sheet whose problems link into `/dsa/theory/<topic>#anchor`, a papers reader, and `/account`. **The CUDA section must reuse these patterns and components, not invent a parallel UI.** TrenTorch's brand is "no black boxes, build it yourself, understand the machinery", so this section teaches the GPU the same way: **explain, visualize, then make the learner write the kernel and see what the hardware would do.**

Three pillars, all cross-linked:

| Pillar | What it is |
|---|---|
| **Theory** | Interactive, visual chapters: GPU architecture → execution model → memory → parallel patterns → advanced topics. |
| **Problems** | A sequenced bank of CUDA kernel problems, solved in the browser. |
| **Solutions** | For every problem: naive → optimized, with the *reason* the final version is optimal, backed by simulator metrics. |

The theory ↔ problem links run in **both directions**: a theory chapter says "now try these problems", and every problem says "read this chapter first (or when stuck)".

### 0.2 Execution engine: Gpubox
All code runs in the browser on **Gpubox**, the team's own simulator (source: `https://github.com/aadityansha06/Gpu-Box`, demo `https://gpu-box.vercel.app`, npm package `gpubox`). Because Gpubox is owned by the team, there is **no licensing blocker**, and any missing feature (a T4 profile, a coalescing metric) can be added directly in that repo. The engine will be self-hosted on a CDN (§8.8). Facts taken from its README and docs, which the plan depends on:

- **Two engines:** (1) a JavaScript SIMT engine that transpiles CUDA C++ ASTs into ES6 generators and steps warps in lockstep coroutines (this is what runs arbitrary learner code and makes `__syncthreads()`, divergence and race detection possible); (2) a C++17 core compiled to WebAssembly with Emscripten (`sim/`, about 192 KB) that is used for **fixed problem harnesses**.

- Install: `npm i gpubox`, or CDN `window.Gpubox`. API: `createSimulator`, `createWorkerSimulator` (Web Worker), `compile`, `analyze`, `run`, `validateOutput` (abs / relative / ULP modes), `sim.getCounters().toJSON()`, `sim.getDiagnostics()`, `sim.on('kernel_start' | 'memcpy' | ...)`.
- It reports bytes moved per memory level, FLOPs, bank conflicts, divergence, races (`raceDetection: true`), out-of-bounds, runaway loops (watchdog), leaks, and multi-GPU NCCL desync/deadlocks.
- Profiles: A100, H100, RTX 4090, RTX 4050 Laptop (hardware-verified), RTX 3090, V100, RTX 5060 Ti (projected). **There is no T4 profile.**
- Not supported (rejected at compile time): inline PTX, WMMA/tensor-core intrinsics, dynamic parallelism, CUDA Graphs. Timing is a roofline *model* (about 2-3x on small kernels), not a measured time.
- Runs fully client-side, so there is no server cost and no code leaves the browser.

### 0.3 Phase 0 checklist (the agent must resolve these before writing features)
Do these, and write the answers into `docs/cuda/DECISIONS.md`.

1. **Locate the website source.** `trentorch.com` is built from some repo or branch (the footer links `blob/TrenTorch-Dev/...`, so check the `TrenTorch-Dev` branch of `TrenTorch/TrenTorch` first). Identify the framework, routing, styling, and how the existing `/ide/<slug>` page, the language dropdown, the Run/Submit flow and the `/dsa/theory/<topic>#anchor` links are implemented. **Extend those; do not rebuild them.** Find out how the **existing C++ option in the IDE executes** (server-side judge? WASM?). That answer decides how much of §8.3.1 Tier 1 is free to reuse.
2. **Own and host Gpubox.** Gpubox is the team's product, so licensing is not an issue. Do (a) read `docs/SECURITY_AND_CSP.md`, `docs/INTEGRATION_GUIDE.md` and `docs/PERFORMANCE.md` in the Gpu-Box repo; (b) decide the CDN plan in §8.8; (c) note that the README itself warns that the JS engine uses `new Function`, so untrusted code needs real sandboxing (§8.3.2). trentorch.com is a public site with accounts, so this is a hard requirement. The CSP exception for `new Function` must be scoped to the CUDA routes only.
3. **Verify the counter fields.** Dump `sim.getCounters().toJSON()` and `sim.getDiagnostics()` for 5 sample kernels (saxpy, tiled matmul, transpose, divergent branch, atomic histogram) and record the exact field names for: global load/store bytes, shared bytes, bank conflicts, divergent branches / warp efficiency, atomics, FLOPs, estimated time. The grader (§8.3) and metric tables depend on them. If a metric is missing (for example a coalescing efficiency ratio), file it as a feature request to Gpubox rather than faking it.
4. **T4 gap.** The user wants a "float vs float4 on a T4" lesson. Options, in order of preference: (a) add a `T4` profile to Gpubox directly in the Gpu-Box repo (`demo/gpu-profiles.js` and the `js/` package; Turing, 40 SMs, 2560 FP32 cores, about 320 GB/s GDDR6, about 8.1 TFLOPS FP32, 16 GB, 64 KB shared/SM, 4 MB L2); (b) use RTX 4050 or V100 in the sim and label it clearly; (c) in addition, ship a **Colab notebook** that runs the same kernels on a real Colab T4 and commit the measured numbers as static JSON that the chart reads. Do (a) or (b) for interactivity and (c) for ground truth. Never present simulator timing as a T4 measurement.
5. **Problem source and copyright.** The problem list references `tensortonic.com/problems/...`. Do **not** copy their statements or solutions verbatim unless the team owns them. Write original statements, starter code, tests and solution write-ups; keep the reference number and URL only as `externalRef` metadata ("inspired by / mirrors problem #88"). If the team owns Tensortonic, record that in `DECISIONS.md` and the restriction goes away.
6. **Do not copy textbook text.** The course follows the *PMPP* book (Hwu, Kirk, El Hajj) in topic order. Map chapters to PMPP chapter numbers for study guidance, but write all explanations, figures and examples originally.
7. **Profile before optimizing.** Measure, for 5 representative kernels, the time spent in (i) loading Gpubox and WASM, (ii) parsing/transpiling the source, (iii) executing each test case, (iv) collecting counters. Record it in `DECISIONS.md`. See §8.3.1: our working hypothesis is that execution, not parsing, dominates, and that fixing repeated parsing is a cache, not a new compiler.

### 0.4 Global engineering rules
- Content is **data in git** (MDX + JSON), validated at build time. No content lives only in a database.
- Every interactive visualization works **without** the simulator when possible (deterministic TypeScript model), and is only simulator-driven where the lesson is about measured behaviour.
- Everything is keyboard-accessible, works at 375px width, respects `prefers-reduced-motion`, and supports dark mode (the TrenTorch brand is dark/orange; reuse the existing theme tokens).
- Never claim more than the simulator or hardware supports. Claims in prose use the careful wording in §6.2 (for example "a compiler *may* lower a short conditional to predication").

---

## 1. Information architecture and routes

Follow the conventions trentorch.com already uses (problems at `/ide/<slug>`, theory at `/dsa/theory/<topic>#anchor`):

```
/cuda                          Landing: roadmap map, progress, "Start theory" / "Jump to problems"
/cuda/theory                   Theory index (parts A–F as a visual roadmap)
/cuda/theory/[chapterSlug]#anchor   One chapter (MDX + visualizations + "Practice" panel); mirrors /dsa/theory/<topic>#anchor
/ide/cuda-[slug]               Problem workspace: the EXISTING IDE page with a new runtime "CUDA (Gpubox)".
                               Tabs reuse Description / Hints / Solution / Discussion; Guide / Editor / Output panels;
                               add an Output sub-tab "Report" (bytes, FLOPs, banks, divergence, certificate)
/problemset?category=cuda      CUDA problems appear in the main problemset with a category filter
/cuda/problems                 Optional curated CUDA-only list (stages, DAG view) linking to /ide/cuda-[slug]
/cuda/playground               Free-form Gpubox playground (reuse the IDE shell, no tests)
/cuda/glossary                 Every term (SIMT, SM, warp, GigaThread, ...) with a link to where it is taught
/cuda/paths                    Curated learning paths ("Theory-first", "Problem-first", "Interview prep", "ML kernels")
```

Add "CUDA" to the **Learn** menu (which currently shows "Roadmap soon") and to the "Browse topics" modules. For CUDA problems the language dropdown shows only `CUDA C++` (Gpubox); the Python/Java/etc. options are hidden.

### 1.1 Two entry modes (the user's requirement)
- **Theory-first:** read a chapter → "Practice this chapter" panel lists linked problems → click opens the problem.
- **Problem-first:** open a problem → if stuck, "Read the theory" opens the linked chapter **scrolled to the relevant section anchor** (not just the page top); a chapter-level "Back to problem" chip remembers where you came from.
- The problems list has a **"Solve directly" vs "Read theory first"** toggle. The second changes the primary button on each row to the problem's top prerequisite chapter.

### 1.2 Link integrity (hard requirement)
A single registry, `content/cuda/registry.ts` (generated at build, never hand-edited), holds every `chapter`, `section anchor`, `problem`, `glossary term` and their relations. A **build-time validator** fails CI if:
- a chapter lists a problem that does not exist, or a problem lists a chapter or anchor that does not exist;
- the relation is one-directional (A lists B, but B does not list A back);
- a problem has no solution write-up or no reference implementation;
- a glossary term is used in MDX via `<Term id="..."/>` but not defined.

---

## 2. Content model

### 2.1 Folder layout (propose; adapt to the site stack found in Phase 0)

```
content/cuda/
  theory/
    A1-why-gpus.mdx
    A2-simt-and-pcie.mdx
    ...                               (see §4 for the full list)
  problems/
    CU-001-vector-addition/
      problem.mdx                     statement, constraints, examples
      meta.json                       see schema below
      starter.cu                      the only thing the learner edits
      harness.ts                      test generation, reference impl, launch config
      tests.json                      visible cases (+ hidden cases flagged)
      hints.mdx                       3-level hint ladder
      solution/
        naive.cu
        optimized.cu
        further.cu                    optional stretch (for example float4)
        solution.mdx                  write-up in the §6 template
        metrics.json                  generated by CI: counters for each variant
  glossary.json
  registry.ts                         GENERATED
components/cuda/
  viz/                                one folder per visualization (§5)
  problem/                            Editor, ResultsPanel, MetricsTable, HintLadder, SolutionTabs
  theory/                             Callout, Term, PracticePanel, ChapterNav, BackToProblem
  sim/                                gpubox wrapper: worker client, runner, metric adapters
lib/cuda/
  progress.ts                         completion state (localStorage first)
  grader.ts                           pipeline from §8.3
scripts/
  validate-content.ts                 link integrity + schema (zod)
  build-metrics.ts                    runs every reference solution in Node, writes metrics.json
  colab/t4_benchmarks.ipynb           real-T4 numbers for the bandwidth lessons
docs/cuda/DECISIONS.md
```

### 2.2 Theory chapter frontmatter

```yaml
id: B3
slug: warps-and-lockstep
title: "Warps: 32 threads that move together"
part: B
order: 3
pmpp: ["Ch. 4"]                 # study pointer only
prereqs: [B1, B2]
terms: [warp, lane, SIMT, warp-scheduler]
viz: [VIZ-WARP-FORMATION, VIZ-LATENCY-HIDING]
problems:                        # bidirectional, validated
  - { id: CU-003, anchor: "branchless-vs-divergence", role: apply }
  - { id: CU-009, anchor: "linearized-thread-id",     role: apply }
estMinutes: 25
```

### 2.3 Problem `meta.json`

```json
{
  "id": "CU-003",
  "slug": "relu",
  "title": "ReLU as a CUDA Kernel",
  "difficulty": "easy",
  "stage": 1,
  "topics": ["map", "memory-bound", "branchless"],
  "externalRef": { "number": 88, "url": "https://www.tensortonic.com/problems/relu", "note": "mirrors, not copied" },
  "trentorchLink": { "module": "02_activations", "note": "GPU version of the NumPy ReLU you built" },
  "theory": [
    { "chapter": "C1", "anchor": "branchless-vs-divergence", "why": "avoid a divergent branch" },
    { "chapter": "D2", "anchor": "arithmetic-intensity",     "why": "why it is memory-bound" }
  ],
  "prereqProblems": ["CU-001"],
  "nextProblems": ["CU-004"],
  "kernelSignature": "relu(const float* in, float* out, int n)",
  "launch": { "mode": "learner-chooses-block", "constraints": { "blockMultipleOf": 32 } },
  "gpuProfile": "A100",
  "lowerBound": { "globalBytes": "8*n", "flops": "n" },
  "grading": { "correctness": "required", "boundsCheck": "required", "efficiencyTarget": "within 1.05x of lowerBound.globalBytes" },
  "unsupportedFeatures": [],
  "solutionUnlock": "after-pass-or-3-attempts"
}
```

`lowerBound` is the key to the "reason why it is optimal" requirement (§6.3).

---

## 3. Learner experience specs

### 3.1 Theory chapter page
- Left: sticky mini-TOC with section anchors; right: content with **inline interactive figures** (not just at the end).
- Components: `<Callout kind="intuition|pitfall|pmpp|try">`, `<Term id>` (hover card + link to glossary), `<Viz id props/>`, `<TryKernel>` (a small editable Gpubox snippet inside the chapter), `<PracticePanel/>` at the end (and a collapsed "Practice for this section" chip after each major anchor).
- **"Check yourself"**: 2-3 quick checks per chapter (predict-the-output, click the diverging lanes, choose the coalesced pattern). Interactive, not a quiz wall.
- Footer: Previous / Next, estimated time, "Mark complete".

### 3.2 Problem workspace
Three panes (stack vertically on mobile):
1. **Statement** (tabs: Description · Hints · Theory · Solution).
2. **Editor** (Monaco, CUDA/C++ syntax; starter code; Reset; Run; Submit; GPU profile selector locked per problem; optional "grid/block" override panel on problems that teach launch configuration).
3. **Results** with tabs: *Tests* (pass/fail per case with expected vs actual diff), *Report* (bytes moved by level, FLOPs, bank conflicts, divergence, estimated time vs roofline, bound classification), *Diagnostics* (race / OOB / deadlock messages pointing at kernel, block, thread), *Memory banks* (for shared-memory problems).

**Hint ladder** (3 levels, never gives the answer): (1) conceptual nudge + link to theory anchor, (2) structural hint (what to allocate, which index), (3) pseudo-code. Using a hint is tracked but not punished.

### 3.3 Run vs Submit
- **Run:** visible tests only, fast, shows the report.
- **Submit:** visible + hidden tests + efficiency check against `lowerBound` + diagnostics must be clean. Marks the problem solved and unlocks the solution.

### 3.4 Progress
- Per-chapter: viewed / complete. Per-problem: not started / attempted / solved / solved-optimal (hit the efficiency target).
- Persist to `localStorage` under a versioned key (`trentorch:cuda:v1`). Design `lib/cuda/progress.ts` behind an interface so accounts/sync can be added later without touching UI.
- Roadmap map on `/cuda` colors nodes by status, and the "Continue" button deep-links to the next unfinished chapter or problem.

---

## 4. THEORY CURRICULUM (the course structure)

Six parts, ordered exactly the way the learner needs the ideas. Chapter IDs are stable keys. For each chapter: concepts, the visualization(s) from §5, the linked problems (problem IDs from §6.1), and PMPP pointer.

### Part A: GPU Foundations (what is this machine?)

| ID | Chapter | Concepts to teach | Viz | Problems | PMPP |
|---|---|---|---|---|---|
| A1 | Why GPUs exist | Latency-oriented CPU vs throughput-oriented GPU; die area spent on cores vs cache/control; the "many simple workers" idea; data-parallel thinking | VIZ-CPU-VS-GPU | none (orientation) | Ch. 1 |
| A2 | SIMT, host and device, PCIe | SIMT vs SIMD; host/device split; kernel launch; **PCIe** as the highway between CPU RAM and GPU VRAM (bandwidth gap vs on-device memory, why you minimize transfers); DMA, pinned memory (preview); unified memory (brief) | VIZ-HOST-DEVICE-PCIE, VIZ-SIMT-LOCKSTEP | CU-001 | Ch. 2 |
| A3 | Inside the chip | **GigaThread Engine** (global block scheduler), **GPCs**, TPCs, **SMs**, SM sub-partitions, **CUDA cores** (FP32/INT32), SFUs, LD/ST units, warp schedulers, register file, L1/shared memory block, L2, memory controllers, HBM/GDDR; tensor cores as awareness only | VIZ-GPU-DIE-EXPLORER (zoom: die → GPC → SM → sub-partition) | none (glossary-heavy) | Ch. 4 |
| A4 | The memory hierarchy at a glance | Registers, local, shared, L1, L2, global, constant; size/latency/bandwidth ladder; "who can see what" (thread/block/grid scope); why data movement dominates | VIZ-MEMORY-LADDER, VIZ-SCOPE-VISIBILITY | CU-001 | Ch. 5 |

### Part B: The programming model (threads → blocks → warps → grid)

| ID | Chapter | Concepts | Viz | Problems | PMPP |
|---|---|---|---|---|---|
| B1 | Threads, blocks, grids and indexing | `threadIdx/blockIdx/blockDim/gridDim`; global index formula; 1D/2D/3D grids; ceil-div launch size; **the bounds check** and what happens without it; row-major mapping of 2D data | VIZ-INDEX-CALCULATOR, VIZ-GRID-BUILDER | CU-001, CU-002, CU-009, CU-010 | Ch. 2-3 |
| B2 | How blocks land on SMs | GigaThread assigns blocks to SMs; blocks are independent; residency limits per SM; waves and the **tail effect**; why you must not assume block order | VIZ-BLOCK-SCHEDULER | CU-001 | Ch. 4 |
| B3 | Warps and lockstep | 32-lane warps; linearization of `threadIdx` (x fastest); warp formation for 1D/2D blocks; warp schedulers issue one instruction for 32 lanes; **zero-cost context switching** → latency hiding | VIZ-WARP-FORMATION, VIZ-LATENCY-HIDING | CU-009, CU-018 | Ch. 4 |
| B4 | Occupancy and resource limits | Threads/SM, blocks/SM, registers/thread, shared mem/block as the limiters; occupancy vs performance (more is not always better); block-size choice (multiple of 32; 128-256 common) | VIZ-OCCUPANCY-CALC | CU-040 (occupancy sweep) | Ch. 4, 6 |
| B5 | The host side | `cudaMalloc/Memcpy/Free`, launch syntax, async nature of launches, `cudaDeviceSynchronize`, error checking, leak detection (Gpubox reports leaks) | VIZ-HOST-TIMELINE | CU-001 | Ch. 2 |

### Part C: Control flow

| ID | Chapter | Concepts | Viz | Problems | PMPP |
|---|---|---|---|---|---|
| C1 | Warp divergence | Masked execution; both paths serialized; reconvergence; when divergence is real vs when a compiler predicates a short conditional (be careful: see §6.2); **branchless idioms** (`fmaxf`, select, predication); divergence cost model (up to 32x on worst case); data-dependent vs index-dependent branches; Volta+ independent thread scheduling (awareness) | VIZ-DIVERGENCE-LANES | CU-003, CU-004, CU-016, CU-044 | Ch. 4, 6 |
| C2 | Barriers and divergent barriers | `__syncthreads()` semantics; barrier inside a divergent branch = hang/UB; shared-memory races (RAW/WAR/WAW) | VIZ-BARRIER-EPOCHS | CU-050 (bug hunt) | Ch. 5 |

### Part D: Memory performance

| ID | Chapter | Concepts | Viz | Problems | PMPP |
|---|---|---|---|---|---|
| D1 | Global memory coalescing | How a warp's 32 addresses become 32/64/128-byte transactions; unit stride best case; strided/misaligned/AoS vs SoA; row- vs column-major access in 2D | VIZ-COALESCING | CU-009, CU-030 (transpose) | Ch. 6 |
| D2 | Roofline: memory-bound or compute-bound | FLOPs per byte; ridge point; classify ReLU (≈0.125 FLOP/byte) vs matmul; what levers apply to each class | VIZ-ROOFLINE | CU-003, CU-005, CU-031 | Ch. 6 |
| D3 | float vs float4 (vectorized access) | 128-bit loads/stores; alignment requirements; fewer instructions and transactions; when it helps (memory-bound maps) and when it does not; **measured on a real T4 (Colab)** and modelled in Gpubox | VIZ-FLOAT4-BANDWIDTH (static T4 data + sim) | CU-012 | Ch. 6 |
| D4 | Shared memory and tiling | On-chip scratchpad; load once, reuse many; `__syncthreads()` after load and before overwrite; tile size vs shared capacity; **when not to use it** (a map has no reuse) | VIZ-TILING-STEPPER | CU-031, CU-032 | Ch. 5 |
| D5 | Bank conflicts | 32 banks; stride-32 worst case; broadcast rule; **padding trick** (`[32][33]`); transpose as the canonical case | VIZ-BANK-GRID | CU-030 | Ch. 5-6 |
| D6 | Registers, local memory, constant and read-only cache | Register pressure and spilling; constant memory broadcast (conv filters); `const __restrict__` | VIZ-REGISTER-PRESSURE | CU-026, CU-027 | Ch. 5, 7 |

### Part E: Parallel patterns (PMPP in order)

| ID | Chapter | Concepts | Viz | Problems | PMPP |
|---|---|---|---|---|---|
| E1 | Map: elementwise kernels | One thread per element; activation functions; fast-math intrinsics (`__expf`) and accuracy tradeoff; RNG per thread (Dropout) | VIZ-MAP-FLOW | CU-001..CU-012 | Ch. 2 |
| E2 | Reduction | Tree reduction; ladder: (1) interleaved divergent, (2) interleaved non-divergent, (3) sequential addressing, (4) first-add-during-load, (5) warp shuffle, (6) multi-block with `atomicAdd` or two-pass; why reductions are the backbone of norms, loss, softmax | VIZ-REDUCTION-TREE | CU-013..CU-021 | Ch. 10 |
| E3 | Row-wise ops | One block per row; block-wide max/sum; **numerically stable softmax**, online softmax; LayerNorm/RMSNorm; cross-entropy via log-sum-exp | VIZ-ROWWISE-SOFTMAX | CU-022..CU-025 | Ch. 10, 16 |
| E4 | Stencils and convolution | Halo cells; boundary handling; constant-memory filter; shared-memory tile with halo; 1D → 2D → 3D; max pooling | VIZ-HALO-TILE | CU-026..CU-029 | Ch. 7-8 |
| E5 | Histogram and atomics | `atomicAdd` contention; privatization in shared memory; coarsening; atomic throughput | VIZ-ATOMIC-CONTENTION | CU-033 | Ch. 9 |
| E6 | Prefix sum (scan) | Inclusive vs exclusive; Hillis-Steele (work-inefficient, simple) vs Blelloch (work-efficient); multi-block scan; uses of scan (stream compaction, radix sort) | VIZ-SCAN-NETWORK | CU-034 | Ch. 11 |
| E7 | **Matrix multiplication ladder** | v1 naive (1 thread/output) → v2 coalescing fix → v3 shared-memory tiling → v4 thread coarsening (multiple outputs/thread) → v5 vectorized (`float4`) loads → v6 register tiling / bank-conflict-free → v7 double buffering (concept). Roofline position at each step. Link to TrenTorch module `03_layers` and `Linear` | VIZ-MATMUL-LADDER | CU-031..CU-037 | Ch. 5-6 |
| E8 | **Sorting day** | Why **quicksort sucks on GPUs**: data-dependent branching → massive warp divergence, irregular recursion, poor load balance; GPU-friendly alternatives: **bitonic sort** (fixed network, zero divergence), **radix sort** (built from scan), merge-based sort; compare operation counts vs divergence | VIZ-QUICKSORT-DIVERGENCE, VIZ-BITONIC-NETWORK | CU-044, CU-045 | Ch. 12-13 |

### Part F: Advanced and systems

| ID | Chapter | Concepts | Viz | Problems | PMPP |
|---|---|---|---|---|---|
| F1 | Warp-level primitives | `__shfl_down_sync`, `__ballot_sync`, warp reductions without shared memory; cooperative groups (awareness) | VIZ-SHUFFLE-NETWORK | CU-046 | Ch. 10, 22 |
| F2 | Streams and overlap | Async copies, pinned memory, overlapping H2D / compute / D2H; PCIe as the bottleneck revisited | VIZ-STREAM-TIMELINE | theory + playground only | Ch. 20, 22 |
| F3 | Kernel fusion and attention | Why fuse (memory traffic saved, count it); fused bias+ReLU; fused softmax; the FlashAttention idea (tile + online softmax, never materialize the NxN matrix). Link to TrenTorch modules `12_attention`, `17_acceleration` | VIZ-FUSION-TRAFFIC | CU-038, CU-039 | Ch. 16, 22 |
| F4 | Multi-GPU and NCCL | AllReduce / Broadcast / AllGather; ring algorithm; topology (NVLink mesh vs PCIe tree); DDP gradient AllReduce; how deadlocks happen | VIZ-RING-ALLREDUCE | CU-047, CU-051 | Ch. 20 |
| F5 | Debugging and profiling mindset | Race / OOB / divergent-barrier / deadlock bug hunts; reading a Gpubox report; roofline-first optimization workflow | none (uses workspace) | CU-048..CU-051 | Ch. 6, 22 |
| F6 | Capstone | Compose: fused MLP block or mini-attention using kernels the learner wrote; bridge back to TrenTorch (call it as the "GPU backend" of Module 17) | VIZ-CAPSTONE-PIPELINE | CU-052 | Ch. 16, 19 |

---

## 5. VISUALIZATION CATALOG

Build each as a self-contained React component in `components/cuda/viz/<id>/`. Pattern: **a pure TypeScript model** (`model.ts`, unit-tested, no DOM) + **a view** (SVG or Canvas, `view.tsx`) + **controls**. Prefer SVG/CSS animation (or `framer-motion`) over heavy 3D. Every viz exposes `playing`, `step`, `reset`, a speed slider, and a text description (`aria-live`) of the current state.

| ID | Used in | What it shows | Interactions | Data source |
|---|---|---|---|---|
| VIZ-CPU-VS-GPU | A1 | Die diagram: few big cores + cache vs many small cores | Toggle workload (serial vs data-parallel) and watch time bars | model |
| VIZ-HOST-DEVICE-PCIE | A2 | CPU RAM ⇄ PCIe ⇄ GPU VRAM with relative bandwidth | Slider for transfer size; shows copy time vs compute time | model |
| VIZ-SIMT-LOCKSTEP | A2, B3 | 32 lanes executing one instruction stream | Step instruction by instruction; per-lane registers shown | model |
| VIZ-GPU-DIE-EXPLORER | A3 | Zoomable die → GPC → SM → sub-partition with labelled units (GigaThread Engine, schedulers, cores, LD/ST, SFU, register file, shared/L1, L2) | Click a unit for a definition and a link into the glossary; profile switch (T4 / A100 / H100) changes counts | static JSON per GPU profile |
| VIZ-MEMORY-LADDER | A4 | Pyramid of memory levels with size / latency / bandwidth | Hover for scope; "send a load" animation falls through levels | static JSON |
| VIZ-SCOPE-VISIBILITY | A4 | Which thread/block can read/write which memory | Click a thread, see reachable memories highlighted | model |
| VIZ-INDEX-CALCULATOR | B1 | Grid of blocks of threads; compute `idx` | Edit `gridDim`, `blockDim`, click a thread to see the formula evaluated; shows idle tail threads when `N` is not a multiple of block size (use the N=6, block=4 example) | model |
| VIZ-GRID-BUILDER | B1 | 2D/3D grid layout over a matrix | Drag to choose block shape; shows row-major mapping | model |
| VIZ-BLOCK-SCHEDULER | B2 | Blocks queued → SMs, with residency limits | Change #SMs and per-SM limits; watch waves and the tail effect | model |
| VIZ-WARP-FORMATION | B3 | How a 2D block (x fastest) is cut into 32-thread warps | Edit block dims; highlight which threads share a warp; show partial warps | model |
| VIZ-LATENCY-HIDING | B3 | Warp scheduler timeline: warps stall on loads, others issue | Slider: warps resident; watch pipeline utilization climb | model |
| VIZ-OCCUPANCY-CALC | B4 | Resource bars (threads, regs, shared) vs SM limits | Edit regs/thread, smem/block, block size; shows limiter and occupancy % | model + profile JSON |
| VIZ-HOST-TIMELINE | B5 | Host launch is async; sync points | Toggle `cudaDeviceSynchronize` | model |
| VIZ-DIVERGENCE-LANES | C1 | 32 lanes, `if/else`, masked execution animating both paths | Pick data pattern (all-positive, alternating, random); show active-mask and cycles used vs ideal; toggle branchy vs `fmaxf` form | model (+ optional sim report) |
| VIZ-BARRIER-EPOCHS | C2 | Threads with shared reads/writes across barriers | Remove a `__syncthreads()` and watch the race light up | model |
| VIZ-COALESCING | D1 | 32 addresses → memory segments | Stride slider (1, 2, 4, 32), offset slider; shows transaction count and efficiency % | model |
| VIZ-ROOFLINE | D2 | Roofline plot with kernels as points | Pick GPU; drag arithmetic intensity; plots ReLU, SAXPY, softmax, matmul versions; **plots the learner's last run** | model + sim counters |
| VIZ-FLOAT4-BANDWIDTH | D3 | Bar/line chart: effective GB/s for float vs float2 vs float4 across array sizes | Switch device (T4 measured / sim); alignment toggle | **static JSON from Colab T4 run** + sim |
| VIZ-TILING-STEPPER | D4 | Matrix tiles marching through shared memory | Step through load / sync / compute / sync; show global loads saved | model |
| VIZ-BANK-GRID | D5 | 32 banks × rows, thread accesses colored | Stride and padding sliders; conflict degree shown; reuse Gpubox's "Memory banks" panel if embeddable | model / sim |
| VIZ-REGISTER-PRESSURE | D6 | Regs/thread vs resident warps | Slider shows spill threshold | model |
| VIZ-MAP-FLOW | E1 | Element → thread mapping for a map kernel | Click element, see thread/warp/block | model |
| VIZ-REDUCTION-TREE | E2 | Tree reduction with active threads | Choose variant 1-6; shows divergence, bank conflicts, idle threads, steps | model |
| VIZ-ROWWISE-SOFTMAX | E3 | One block per row: max → exp → sum → divide | Toggle stable/unstable; show overflow; show online softmax single pass | model |
| VIZ-HALO-TILE | E4 | Tile + halo loaded into shared memory | Filter-size slider; shows loads per output with/without tiling | model |
| VIZ-ATOMIC-CONTENTION | E5 | Threads hitting bins | Bin-count and data-skew sliders; global vs privatized cost | model |
| VIZ-SCAN-NETWORK | E6 | Hillis-Steele and Blelloch networks | Switch algorithm; shows work and depth counts | model |
| VIZ-MATMUL-LADDER | E7 | One panel per version v1..v7: access pattern, bytes, roofline point | Scrub the ladder; table of global loads, shared bytes, estimated time from sim | model + sim |
| VIZ-QUICKSORT-DIVERGENCE | E8 | Quicksort partition on a warp: lanes diverge on `< pivot`; recursion imbalance | Array size/shape; lane utilization % over time; side-by-side with bitonic | model |
| VIZ-BITONIC-NETWORK | E8 | Fixed compare-exchange network | Step through stages; shows zero divergence | model |
| VIZ-SHUFFLE-NETWORK | F1 | Lane-to-lane register exchange | Step `shfl_down` offsets | model |
| VIZ-STREAM-TIMELINE | F2 | H2D / kernel / D2H timelines for 1..4 streams | Chunk size slider | model |
| VIZ-FUSION-TRAFFIC | F3 | Bytes saved by fusing kernels | Toggle fusion; counts HBM round-trips | model + sim |
| VIZ-RING-ALLREDUCE | F4 | Ring algorithm across N GPUs | N slider (2-16), topology toggle | model (+ Gpubox `allReduce` counters) |
| VIZ-CAPSTONE-PIPELINE | F6 | Dataflow of the capstone pipeline | Highlight which learner kernel runs where | model |

**Build order for visualizations:** start with the five that carry the most teaching weight and are needed by early problems: INDEX-CALCULATOR → WARP-FORMATION → DIVERGENCE-LANES → COALESCING → ROOFLINE. Then the rest in chapter order. Share primitives (a `LaneStrip` showing 32 lanes, a `MemoryCell` grid, a `Stepper` control bar) across them to keep the style consistent.

---

## 6. PROBLEMS AND SOLUTIONS

### 6.1 Problem bank, in recommended order
`externalRef` = the number from the user's reference list. Rows marked **NEW** are not in that list and must be authored for this course. Difficulty follows the reference list; new problems get a difficulty from the author.

**Stage 1: Map and indexing (Part B, C1, D1-D3, E1)**

| ID | Slug | Title | Ref # | Diff | Key lesson |
|---|---|---|---|---|---|
| CU-001 | vector-addition | Vector Addition | 590 | Easy | Global index, bounds check, host/device flow |
| CU-002 | hadamard-product | Hadamard Product | 277 | Easy | Map with two inputs, 12N bytes bound |
| CU-003 | relu | ReLU | 88 | Easy | Branchless `fmaxf`, memory-bound |
| CU-004 | leaky-relu | Leaky ReLU | 206 | Easy | Select vs branch, predication |
| CU-005 | sigmoid | Sigmoid | 279 | Easy | `expf` vs `__expf`, SFU, accuracy |
| CU-006 | tanh | Tanh | 526 | Easy | Intrinsic accuracy tradeoff |
| CU-007 | swish | Swish (SiLU) | 55 | Easy | Fused elementwise, one pass |
| CU-008 | gelu | Exact GELU | 387 | Easy | `erff` use, compute per byte rises |
| CU-009 | matrix-addition | Matrix Addition | 139 | Easy | 2D indexing, x as the fast axis, coalescing |
| CU-010 | outer-product | Outer Product | 96 | Easy | 2D grid, broadcast reuse of two vectors |
| CU-011 | dropout | Dropout | 358 | Easy | Per-thread hash RNG, determinism with a seed |
| CU-012 | relu-float4 | **NEW** ReLU with float4 | n/a | Medium | Vectorized loads, alignment, tail handling (ties to D3 and the T4 lesson) |

**Stage 2: Reductions (E2, F1)**

| ID | Slug | Title | Ref # | Diff | Key lesson |
|---|---|---|---|---|---|
| CU-013 | sum-of-array | Sum of Array | 271 | Easy | Shared-memory tree, then `atomicAdd` across blocks |
| CU-014 | max-of-array | Max of Array | 542 | Easy | Reduction with a non-additive op; atomicMax on float needs care |
| CU-015 | min-of-array | Min of Array | 199 | Easy | Same pattern, identity element choice |
| CU-016 | argmax | Argmax | 107 | Medium | Reducing (value, index) pairs, tie-breaking rule |
| CU-017 | dot-product | Dot Product: Multi-Block Reduction | 452 | Medium | Grid-stride loop + block reduce + final combine |
| CU-018 | mean-variance | Mean and Variance | 163 | Medium | Two-pass vs Welford; numerical stability |
| CU-019 | l1-normalize | L1 Normalization | 335 | Medium | Reduce then map; two kernels or one with grid sync trade-off |
| CU-020 | l2-normalize | L2 Normalization | 606 | Medium | Sum of squares, `rsqrtf` |
| CU-021 | cosine-similarity | Cosine Similarity | 361 | Medium | Three reductions fused into one pass |

**Stage 3: Row-wise normalization and losses (E3)**

| ID | Slug | Title | Ref # | Diff | Key lesson |
|---|---|---|---|---|---|
| CU-022 | softmax | Softmax | 301 | Medium | Stable (subtract max), block per row, then online softmax |
| CU-023 | rms-norm | RMS Normalization | 111 | Medium | Block-per-row reduce, `rsqrtf` |
| CU-024 | layer-norm | Layer Normalization | 218 | Medium | Mean and variance in one pass, affine params |
| CU-025 | cross-entropy | Cross-Entropy Loss | 558 | Medium | Log-sum-exp, avoid overflow, per-row reduce |

**Stage 4: Stencils (E4, D6)**

| ID | Slug | Title | Ref # | Diff | Key lesson |
|---|---|---|---|---|---|
| CU-026 | conv-1d | 1D Convolution | 512 | Easy | Halo, bounds, constant filter |
| CU-027 | conv-2d | 2D Convolution | 501 | Medium | 2D tile + halo in shared memory |
| CU-028 | max-pool-2d | Max Pool 2D | 593 | Medium | Windowed reduce, stride handling |
| CU-029 | conv-3d | 3D Convolution | 142 | Hard | 3D indexing, shared tile limits |

**Stage 5: Memory patterns, scan, histogram, sorting (D1, D5, E5, E6, E8)**

| ID | Slug | Title | Ref # | Diff | Key lesson |
|---|---|---|---|---|---|
| CU-030 | transpose | **NEW** Matrix Transpose | n/a | Medium | Naive (uncoalesced) → shared tile → padded `[32][33]`, zero bank conflicts |
| CU-033 | histogram | **NEW** Histogram | n/a | Medium | Global atomics → shared privatization |
| CU-034 | prefix-scan | **NEW** Prefix Sum (Scan) | n/a | Hard | Hillis-Steele then Blelloch; multi-block |
| CU-044 | bitonic-sort | **NEW** Bitonic Sort | n/a | Hard | Fixed network, no divergence |
| CU-045 | radix-sort | **NEW** Radix Sort (via scan) | n/a | Hard | Scan-based partition; contrast with quicksort |

**Stage 6: Matrix multiplication ladder (E7, D4, D2)**

| ID | Slug | Title | Ref # | Diff | Key lesson |
|---|---|---|---|---|---|
| CU-031 | matmul | Matrix Multiplication | 308 | Medium | Naive baseline; count global loads (2K per output) |
| CU-032 | tiled-matmul | Tiled Matrix Multiplication | 117 | Hard | Shared tiles, two `__syncthreads()`, bounds on edge tiles |
| CU-035 | matmul-coarsened | **NEW** Matmul with Thread Coarsening | n/a | Hard | More outputs per thread, register reuse |
| CU-036 | matmul-vectorized | **NEW** Matmul with float4 + Bank-Free Tiles | n/a | Hard | Vector loads, padding |
| CU-037 | matmul-bias-relu | **NEW** Fused MatMul + Bias + ReLU | n/a | Hard | Fusion saves a full round trip (ties to `Linear` in Module 03) |

**Stage 7: Advanced and systems (B4, F1-F6)**

| ID | Slug | Title | Ref # | Diff | Key lesson |
|---|---|---|---|---|---|
| CU-038 | fused-softmax-rows | **NEW** Fused Scale + Mask + Softmax | n/a | Hard | One pass, bytes counted |
| CU-039 | attention-lite | **NEW** Mini Attention (QKᵀ, softmax, ·V) | n/a | Hard | Ties to Module 12; online softmax idea |
| CU-040 | occupancy-sweep | **NEW** Block-Size Sweep | n/a | Medium | Use the report to pick a block size and justify it |
| CU-046 | warp-shuffle-reduce | **NEW** Warp-Shuffle Reduction | n/a | Medium | `__shfl_down_sync`, no shared memory |
| CU-047 | multi-gpu-allreduce | **NEW** Multi-GPU AllReduce | n/a | Medium | `ncclAllReduce`, ring counters (Gpubox supports it) |
| CU-048 | bug-shared-race | **NEW** Bug Hunt: Shared-Memory Race | n/a | Medium | Find the missing barrier |
| CU-049 | bug-out-of-bounds | **NEW** Bug Hunt: Out-of-Bounds | n/a | Easy | Missing bounds check |
| CU-050 | bug-divergent-barrier | **NEW** Bug Hunt: Divergent Barrier | n/a | Medium | `__syncthreads()` inside a branch |
| CU-051 | bug-nccl-deadlock | **NEW** Bug Hunt: NCCL Deadlock | n/a | Hard | Rank/order mismatch |
| CU-052 | capstone-mlp-block | **NEW** Capstone: Fused MLP Block | n/a | Hard | Compose earlier kernels; bridge to Module 17 |

> The IDs are not strictly sequential in the table by design (they follow the chapter map in §4). The **display order** on `/cuda/problems` is the table order above, driven by `stage` then `order` fields in `meta.json`. Gpubox already ships example kernels for vector add, SAXPY, ReLU, reduction, softmax, layernorm, tiled matmul, prefix scan, bank-conflict transpose, warp reduction, atomic histogram, multi-GPU AllReduce, DDP, and the four bug programs. Use them as seeds, rewritten to this course's style and harness.

### 6.2 Solution write-up template (derived from the ReLU document supplied by the user)
Every `solution.mdx` follows this skeleton so the whole bank reads consistently. Section names are fixed so that the **theory chapters can deep-link to them**.

1. **Parallelization Strategy**: decomposition (one thread per element / block per row / tile per block), index formula, grid sizing, why the guard exists.
2. **Memory Hierarchy and Access Pattern**: what goes in registers / shared / global and why; coalescing analysis.
3. **Memory-Bound or Compute-Bound?**: FLOPs, bytes, arithmetic intensity, roofline classification, and therefore *which optimizations matter*.
4. **The Key Design Choice** (the "whole point" of the problem; for ReLU: branchless select vs divergence).
5. **Hardware Utilization and Latency Hiding**: occupancy, warps in flight, resource limits.
6. **Naive vs Optimized**: variants compared with **measured simulator metrics** (table) and the next-step refinements (grid-stride, `float4`, fusion).
7. **Worked Example**: a tiny hand-traceable case (like the N=6, block=4 ReLU example).
8. **Pitfalls**: 3-5 bullet points, each tied to a diagnostic Gpubox can raise.

**Editorial rules for the agent (learned from the supplied ReLU draft):**
- Keep the careful wording about divergence: a source-level `if` **may** compile to a predicated/select instruction, so claim "removes the divergence hazard", not "always diverges". Keep that hedge in the Worked Example and Pitfalls as well.
- Use correct math rendering (KaTeX via `remark-math` + `rehype-katex`). The supplied draft contains doubled math (for example `N N`, `⌈N/256⌉ ⌈N/256⌉`), which is a copy-paste artifact of rendered + raw LaTeX. **Strip all such duplicates.** Write `$\lceil N/256 \rceil$` once.
- State quantities precisely (for example 8 bytes per element = one 4-byte load + one 4-byte store; ≈0.125 FLOP/byte). Do not hand-wave "orders of magnitude"; say how far below the ridge point and for which GPU profile, with numbers from the profile JSON.

### 6.3 "Why this is optimal": the optimality certificate
Each problem declares a `lowerBound` (see §2.3). After a run, the Results panel shows a **certificate**:

```
Global bytes moved:     8,192,000   lower bound 8·N = 8,192,000   → 100% of minimum
Bank conflicts:         0
Divergent warps:        0
Bound:                  memory-bound (0.125 FLOP/byte; ridge ≈ N FLOP/byte on A100)
Estimated time (model): 4.1 µs   roofline floor: 4.0 µs   → 97%
```

Lower bounds to define per problem family: map = (inputs + outputs) · 4 bytes; reductions = N·4 bytes read + O(blocks) writes; softmax/norm rows = read once + write once; tiled matmul global loads = 2·M·N·K/TILE · 4 bytes (vs 2·M·N·K·4 for naive); transpose = 2·M·N·4 bytes with zero bank conflicts. `solution.mdx` quotes these numbers directly from `metrics.json`, so prose and data cannot drift.

### 6.4 Solution gating and tabs
- Unlock when the problem is solved **or** after 3 failed submits **or** an explicit "I give up, show me" (confirmation dialog, tracked).
- Tabs: **Naive** · **Optimized** · **Further** (optional) · **Why it's optimal** (the write-up) · **Compare** (metrics table, naive vs optimized, plus a "Run this solution in the editor" button that loads the code and runs the same harness).
- At the bottom: "Read the theory behind this" (chapter anchors from `meta.theory`) and "Next problem".

---

## 7. THEORY ↔ PROBLEM CROSS-LINKING (UX detail)

| From | To | Mechanism |
|---|---|---|
| Chapter section | Problems | `<PracticeChip problems={["CU-003","CU-004"]}/>` after the anchor; and a full `PracticePanel` at chapter end listing all with difficulty and status badges |
| Problem | Chapter section | "Theory" tab lists `meta.theory[]` with the *why* sentence; the editor toolbar has a **📖 Theory** button deep-linking to `/cuda/theory/<slug>#<anchor>` in a side drawer (so the learner does not lose their code) |
| Solution page | Chapter section | "Read the theory behind this" |
| Problem | Problem | `prereqProblems` / `nextProblems` form a DAG shown on `/cuda/problems` as an optional graph view |
| Glossary term | First teaching location | Each term links to the chapter anchor where it is taught |
| Any `<Term id>` | Glossary hover card | Short definition + link |

State across navigation: opening theory from a problem preserves the editor buffer (store per problem in `localStorage`, debounced), and the "Back to problem" chip restores it.

---

## 8. SYSTEM DESIGN

### 8.1 High-level architecture

```
┌──────────────────────────── Browser ────────────────────────────┐
│  Site (Next.js/MDX)                                              │
│   ├─ Theory pages  ── <Viz/> components (pure TS models)         │
│   ├─ Problem page  ── Monaco editor ─┐                           │
│   │                                  ▼                           │
│   │                       lib/cuda/grader.ts                     │
│   │                                  │ postMessage               │
│   │                       ┌──────────▼───────────┐               │
│   │                       │  Web Worker          │               │
│   │                       │  gpubox (createWorker│               │
│   │                       │  Simulator)          │               │
│   │                       └──────────┬───────────┘               │
│   │                                  │ result + counters         │
│   │                       Results UI (tests, report, certificate)│
│   └─ Progress store (localStorage, versioned)                    │
└──────────────────────────────────────────────────────────────────┘
Build time (CI): validate-content.ts · build-metrics.ts (runs all reference solutions in Node
via gpubox, writes metrics.json) · registry generation · Colab T4 JSON checked in.
```

No backend is required for v1. Everything is static + client-side compute, which matches Gpubox's "0 bytes sent to any server" model and keeps hosting free on Vercel.

### 8.2 Tech choices
- **Framework:** whatever Phase 0 finds (reuse the existing `/ide` shell, Monaco setup if present, Run/Submit buttons, hint/solution tabs and progress tracking already on trentorch.com); target Next.js (App Router) + MDX (`@next/mdx` or `contentlayer`/`velite`) with `remark-math`, `rehype-katex`, `rehype-slug`.
- **Editor:** `@monaco-editor/react`, loaded lazily with `dynamic(..., { ssr: false })` only on problem and playground routes (keep theory pages light).
- **Viz:** React + SVG, `framer-motion` for step animation, `d3-scale`/`d3-shape` for the roofline and bandwidth plots; no WebGL needed.
- **Validation:** `zod` schemas for frontmatter and `meta.json`; a Node script run in CI and in a pre-commit hook (the repo already has `.pre-commit-config.yaml` and `.git-hooks`, so add it there).
- **Testing:** Vitest for viz models and the grader; Playwright for end-to-end (open problem → paste solution → submit → solved) and for link-integrity smoke tests.
- **State:** a tiny store (`zustand`) wrapping the progress interface.

### 8.3.0 Engine strategy: parse once, run many, and where a real C++ compiler fits

**The question raised:** the same C++/CUDA source is parsed again and again; why not use a normal C++ compiler (the one behind the TrenTorch DSA C++ option) and then check for CUDA?

**Position:** a real C++ compiler is useful for part of the pipeline but **cannot replace the simulator**, and the repeated parsing should be fixed with caching. Reasons:

1. **It will not compile CUDA as-is.** `__global__`, `<<<grid, block>>>`, `threadIdx`, `__shared__` and `__syncthreads()` are not C++. `g++` rejects the launch syntax outright. `clang -x cuda` accepts it, but only if you also supply fake CUDA headers (Gpubox's `sim/include/cuda_sim.h` is exactly such a shim). So a "normal C++ compiler" still needs a CUDA front-end or a rewrite pass, which is parsing again.
2. **Compiling is not simulating.** A native/WASM build of the kernel gives correct output for simple maps. It gives none of what this course teaches: bytes moved per level, bank conflicts, divergence, races, out-of-bounds with block/thread coordinates.
3. **`__syncthreads()` needs coroutines.** All threads in a block must reach the barrier before any proceeds. A straight compile runs threads one after another (barrier semantics break) unless the kernel is transformed into resumable coroutines. That transformation is the reason Gpubox's JS engine parses the AST into ES6 generators and steps warps in lockstep; the lockstep is also what makes divergence measurable.
4. **Probably the wrong bottleneck.** Parsing a 30-line kernel is cheap. The costly part is executing thousands of simulated threads, per test case. Profile first (Phase 0 item 7).

**What we do instead (tiers):**

| Tier | What | When it runs | Notes |
|---|---|---|---|
| T0 | **Compile cache + warm worker.** Parse/transpile once per distinct source (key = hash of source + engine version); reuse the compiled kernel for every test case and every Run of unchanged code; keep the Worker and WASM module warm; never compile on keystroke | Every Run/Submit | Removes the "again and again" parsing. Pure Gpubox/site change, no new infrastructure |
| T1 | **Optional real-compiler diagnostics:** `clang -x cuda -fsyntax-only` with the shim headers, reusing the DSA C++ toolchain *if* it is WASM or an already-paid server judge | On Run, before simulation, only if cheap | Better error messages than a custom parser. Skip if the DSA C++ runner is server-side and costly, or if it would send learner code off-device |
| T2 | **Gpubox WASM engine for fixed harnesses:** reference solutions, CI `build-metrics`, the optimality certificate baselines, and large-N "scaling" runs where the code is ours | CI and solution pages | Fast, trusted code, so no sandbox needed |
| T3 | **Real hardware, offline:** Colab/nvcc runs that produce the committed `t4-measured.json` | Authoring time | Ground truth for D3 and the matmul ladder; never run per learner |

**Decision rule:** ship T0 first (it is mandatory), measure, then add T1 only if error-message quality is a real complaint. Do not move learner execution off the simulator.

### 8.3.2 Running untrusted learner code safely
Gpubox's own README says the JS engine uses dynamic function evaluation and that Web Workers alone do not stop CPU exhaustion or infinite loops. So: (1) run each submission in a **dedicated Worker inside a sandboxed iframe** served from a separate origin or `sandbox` attribute, no network, no cookies; (2) a **hard wall-clock timeout** enforced from the main thread that `terminate()`s the Worker and spawns a fresh one; (3) a cap on grid size, total threads, loop iterations (Gpubox's watchdog) and memory; (4) learner code never touches `/account` state or tokens, and grading results are only trusted for progress display (hidden tests here prevent cheating at the UI level, not security).

### 8.3 Grader pipeline (`lib/cuda/grader.ts`)
For a submission of `starter.cu` code:
1. **Static check:** `analyze(source)`. Reject unsupported features with a friendly message ("Tensor-core intrinsics are not simulated here, see theory chapter A3").
2. **Signature check:** the kernel name and parameter list must match `meta.kernelSignature`; the fixed host wrapper (owned by `harness.ts`) allocates, copies, launches, and reads back. The learner only edits the kernel (and, for launch-config problems, the grid/block panel).
3. **Compile once per submission** in the worker, through the T0 cache (§8.3.0): hash the source; on a hit, reuse the compiled kernel. Surface compile errors with line numbers mapped back to the learner's code.
4. **Execute** each test case against the already-compiled kernel in a **fresh simulator instance** (fresh memory and counters, shared compiled code) (`raceDetection: true`, watchdog on, per-run timeout). Inputs are generated by `harness.ts` from a seed; the reference result is computed in TypeScript.
5. **Compare** with `validateOutput` using the per-problem tolerance (`abs`, `relative` or `ulp`). Reductions use a tolerance that accounts for summation order.
6. **Collect metrics** from `getCounters()` and `getDiagnostics()`; adapt them through `sim/metricAdapter.ts` (the single place that knows Gpubox field names; see Phase 0 item 3).
7. **Efficiency check** against `lowerBound` and compute the certificate.
8. **Produce feedback**: failing cases first (index, expected, got), then diagnostics (race / OOB / divergent barrier with kernel, block, thread), then the efficiency gap with a pointer to the theory anchor most relevant to that gap. Example: global bytes 2x above the lower bound on a map → link D1 (coalescing) and E1.

**Test-size policy:** the simulator executes threads in JS, so keep test sizes modest (typically ≤ 4,096 elements for maps, ≤ 64×64 for matmul, ≤ 1,024 for scan/sort). Always include an edge case where `N` is **not** a multiple of the block size (to catch missing bounds checks), a case with `N < blockDim`, and negative/zero/NaN-free-by-design data unless the problem is about them. Larger "scaling" numbers shown in the UI come from the roofline model, labelled as modelled.

**Hidden tests:** shipped in the bundle (this is an educational site, not a competition); they only prevent hard-coding visible outputs. Don't spend effort on anti-cheat beyond that.

### 8.4 Reference solutions in CI
`scripts/build-metrics.ts` loads every `naive.cu` / `optimized.cu` / `further.cu`, runs them through the same harness in Node, **asserts they pass**, and writes `metrics.json`. CI fails if (a) any reference fails, (b) `optimized` does not beat `naive` on the stated metric, or (c) `optimized` misses its own `lowerBound` target. This keeps "reason why it's optimal" honest.

### 8.5 Real-T4 data (for D3 and the matmul ladder)
`scripts/colab/t4_benchmarks.ipynb` compiles and times: `relu` (float vs float2 vs float4), SAXPY, vector add, a bandwidth sweep over array sizes, naive vs tiled matmul. It exports `content/cuda/data/t4-measured.json` with GPU name, driver, CUDA version, date and raw medians over N runs. `VIZ-FLOAT4-BANDWIDTH` reads that file and labels it "measured on T4 (Colab, <date>)", next to the clearly-labelled simulator curve.

### 8.6 Performance, accessibility, SEO
- Lazy-load Monaco, Gpubox and viz bundles per route; theory pages must stay under a sensible JS budget (target Lighthouse performance ≥ 90 on mobile for theory pages).
- Server-render the MDX text so chapters are indexable; visualizations hydrate on the client.
- Every viz has a text equivalent; color is never the only channel (use patterns/labels for active/inactive lanes).
- Add OpenGraph images per chapter and problem (title + difficulty + a small viz thumbnail).

### 8.7 Integration with the rest of TrenTorch (light touch, optional later)
- Each CUDA problem with a `trentorchLink` shows a chip "You built this in NumPy in Module 02".
- Later: a `tren cuda` CLI subcommand that lists problems and opens the browser at the right page. Out of scope for v1; keep the registry JSON exportable so the CLI can read it.

### 8.8 Hosting Gpubox on a CDN
Source: `aadityansha06/Gpu-Box` (`js/` is the npm package `gpubox`; `sim/` the C++17 WASM core; `GpuBox-site/` is the marketing site, not the engine).
1. Build with `cd js && npm run build` (outputs ESM, CJS, UMD, types and `public/` WASM assets). Tag a release; **every release is immutable**.
2. Publish to npm (jsDelivr then serves it) **or** upload `dist/` + the `.wasm` to your own static host/CDN under a versioned path such as `https://cdn.trentorch.com/gpubox/1.x.y/`. Prefer the own-host option for the site so it does not depend on `@latest`.
3. **Pin the version** in the site (never `@latest`); keep the version in the compile-cache key (§8.3.0) so an engine upgrade invalidates cached kernels. Add Subresource Integrity hashes for the script.
4. Serve `.wasm` with `Content-Type: application/wasm`, long immutable cache headers, and CORS headers allowing trentorch.com; make sure the Worker script is same-origin or loaded via a Blob/URL the CSP allows.
5. Load Gpubox **only** on CUDA routes (`/cuda/*`, `/ide/cuda-*`), lazily, and show a progress indicator for the first WASM download. Add a CI smoke test that loads the pinned CDN URL and runs `vectorAdd`.
6. Keep a rollback path: the previous pinned version stays on the CDN.

---

## 9. ROADMAP, TASKS AND ACCEPTANCE CRITERIA

### Phase 0: Discovery (½ day)
Tasks: resolve §0.3 items 1-6; write `DECISIONS.md`; spike Gpubox in the site (one route running `vectorAdd` in a worker).
**Done when:** a throwaway `/cuda/spike` page compiles, runs, validates and prints counters in the deployed preview, the counter field names are documented, the timing profile from item 7 is recorded, and it is known how the existing IDE's C++ option executes.

### Phase 1: Skeleton and content pipeline
Tasks: routes from §1; MDX pipeline; zod schemas; registry generator; link validator; layout, nav, theme; `Term`, `Callout`, `PracticePanel`, `ChapterNav`; glossary page seeded with ≥ 40 terms (SIMT, GigaThread Engine, GPC, TPC, SM, warp, lane, block, grid, occupancy, coalescing, bank, divergence, reconvergence, predication, roofline, arithmetic intensity, PCIe, HBM, L1/L2, register spill, atomic, shuffle, NCCL, ...).
**Done when:** CI fails on a deliberately broken cross-link; `/cuda` and `/cuda/theory` render with placeholder chapters.

### Phase 2: Problem engine
Tasks: Monaco editor; Gpubox worker client; grader pipeline §8.3; Results panel (Tests, Report, Diagnostics, Certificate); hint ladder; progress store; solution gating and tabs; `build-metrics.ts`.
**Done when:** CU-001 (vector add) and CU-003 (ReLU) are fully playable end to end, including a failing case with no bounds check that shows an OOB diagnostic naming block and thread, and CI regenerates their `metrics.json`.

### Phase 3: Part A-C content (architecture, programming model, divergence)
Tasks: chapters A1-A4, B1-B5, C1-C2; visualizations in the priority order from §5 plus GPU-DIE-EXPLORER, MEMORY-LADDER, HOST-DEVICE-PCIE, SIMT-LOCKSTEP, BLOCK-SCHEDULER, LATENCY-HIDING, OCCUPANCY-CALC, BARRIER-EPOCHS; Stage 1 problems CU-001..CU-011 with full solutions in the §6.2 template.
**Done when:** a learner can read A1 → C1 and solve CU-001..CU-011 using bidirectional links, every viz has tests for its model, and the glossary links resolve.

### Phase 4: Part D (memory performance) and Stage 2-3 problems
Tasks: chapters D1-D6 including the T4 notebook and `t4-measured.json` (and a Gpubox T4 profile if approved); VIZ-COALESCING, ROOFLINE, FLOAT4-BANDWIDTH, TILING-STEPPER, BANK-GRID, REGISTER-PRESSURE; CU-012, CU-030; Stage 2 (reductions) and Stage 3 (row-wise) problems and chapters E1-E3.
**Done when:** the ROOFLINE viz plots the learner's own last run; the float4 chart renders measured T4 data with provenance; the reduction ladder shows six variants with measured metrics.

### Phase 5: Parallel patterns and the matmul ladder
Tasks: chapters E4-E8; stages 4-6 problems; VIZ-HALO-TILE, ATOMIC-CONTENTION, SCAN-NETWORK, MATMUL-LADDER, QUICKSORT-DIVERGENCE, BITONIC-NETWORK; new problems CU-033, CU-034, CU-035..CU-037, CU-044, CU-045.
**Done when:** the matmul ladder page shows v1 → v6 with bytes and roofline position from `metrics.json`, and the "Sorting Day" chapter demonstrates quicksort lane utilization vs bitonic side by side.

### Phase 6: Advanced and systems
Tasks: chapters F1-F6; CU-038..CU-040, CU-046..CU-052; multi-GPU viz and problems using Gpubox NCCL; bug-hunt problems; capstone and link into Module 17.
**Done when:** all four bug-hunt problems are solvable by reading Gpubox diagnostics, and the capstone passes using only learner-written kernels.

### Phase 7: Polish and launch
Tasks: paths page; search (static index, for example `flexsearch` or Pagefind); a11y audit; Lighthouse; OG images; analytics events (chapter completes, problem solves, theory-from-problem clicks, solution unlocks); README section in the main repo; announce.
**Done when:** every item in the Global Definition of Done passes.

### Global Definition of Done
- [ ] `validate-content` passes: all links bidirectional, all problems have reference solutions and write-ups, all glossary terms resolve.
- [ ] Every reference solution passes its own harness and meets its `lowerBound` target in CI.
- [ ] Every solution page follows the §6.2 template and quotes numbers from `metrics.json`.
- [ ] Every visualization has: model unit tests, keyboard control, reduced-motion behavior, a text description, mobile layout.
- [ ] No claim of real-hardware timing without the Colab-measured provenance label.
- [ ] Gpubox served from a pinned, SRI-checked CDN path; `new Function` CSP exception limited to CUDA routes; learner code runs in a sandboxed Worker with a hard timeout.
- [ ] Lighthouse mobile ≥ 90 on theory pages; Monaco and Gpubox only load on problem/playground routes.
- [ ] Playwright e2e: theory → problem → solve → solution → back to theory, and problem → theory → back-to-problem keeping the editor buffer.

### Suggested team split
1. **Platform:** Phases 0-2 (pipeline, grader, editor).
2. **Content A:** chapters and problems for Parts A-D.
3. **Content B:** Parts E-F, matmul ladder, sorting.
4. **Viz:** the visualization catalog (shared primitives first).
5. **Gpubox owner (you):** counters, T4 profile, any missing metrics, CDN publishing. Changes land in `aadityansha06/Gpu-Box`.

### Risks and mitigations
| Risk | Mitigation |
|---|---|
| Gpubox lacks a metric a lesson needs (coalescing ratio, warp efficiency) | Phase 0 item 3 finds it early; request the metric; fall back to a model-only viz and say so |
| Simulator speed on large inputs | Small harness sizes (§8.3); modelled scaling numbers clearly labelled; compile cache + warm worker (§8.3.0); WASM engine for trusted code |
| Untrusted code on a public site | Sandboxed iframe + Worker + hard timeout/terminate + resource caps (§8.3.2) |
| Gpubox CDN version drift | Pinned immutable versions, SRI, version in the cache key (§8.8) |
| Simulator timing mistaken for hardware timing | Separate "modelled" and "measured (Colab T4)" labels everywhere |
| CSP / `new Function` blocked in production | Detect in Phase 0 spike on a Vercel preview, not locally |
| Content volume (≈ 30 chapters, ≈ 50 problems, ≈ 35 viz) | Ship in the phase order above; each phase is independently releasable; hide unfinished chapters behind `status: draft` in frontmatter |
| Copying external problem text or book text | §0.3 items 5 and 6; originals only |
