# CUDA section: Phase 0 decisions

Status: partial. Working branch is `TrenTorch-Web-Dev` (owner decision); existing IDE components are reused. Items marked OPEN need external access or a human decision.

## 0.3.1 Website source (RESOLVED, corrected on `TrenTorch-Web-Dev`)
An earlier draft described `TrenTorch-Dev`, which lacks most of the site. On **`TrenTorch-Web-Dev`** (the working branch):
- **SvelteKit 2 + Svelte 5 + Tailwind 4**, `adapter-static` (fully prerendered), Vercel. Not Next.js.
- Layout: `platform/` (routes, components), `processes/` (logic), `data/` (content).
- IDE `/ide/[id]` is multi-language (python, sql, javascript, cpp, java, go, rust) with CodeMirror 6. Each language has a `*-service.ts` and `*-worker.ts` in `processes/code-execution/`, sharing `workerRunner`. C++ runs clang compiled to WebAssembly in a Worker (about 29 MB, `static/cpp-runtime`), client-side.
- DSA theory: `data/app_data/14-dsa-sheet/<step>/theory.md`, rendered by `processes/dsa-theory/read-theory.ts` (marked, KaTeX, DOMPurify, heading anchors) at `/dsa/theory/[step]`.
- No Monaco, MDX or zustand: plan items map to the existing Svelte equivalents.

## Decisions taken
1. CUDA becomes a Gpubox-backed service in the style of `cpp-service`, not a new IDE. IDE integration (language option, starters, harness) comes after the spike.
2. Theory chapters live in `data/cuda/theory/<NN-slug>/{meta.json,theory.md}` (outside `data/app_data`, so the curriculum build ignores them) and reuse the DSA renderer (`listTheoryStepsIn(dir)`). The reader UI was extracted to `platform/components/TheoryReader.svelte`, shared with `/dsa/theory`.
3. Gpubox is vendored under `platform/static/gpubox/1.0.0-tt1/` (immutable path; version is part of the compile-cache key). Own CDN and SRI are future work.
4. Real clang syntax diagnostics (tier 1) are now feasible since clang-wasm ships with the site; deferred until error-message quality is a real complaint.

## Open items
- 0.3.5 / 0.3.6 Copyright: original problem and chapter text; keep Tensortonic numbers only as `externalRef`. Confirm Tensortonic ownership.
- CSP: none configured today. When added, `unsafe-eval` is needed only by `/gpubox/worker.js`.
- Colab T4 notebook and `t4-measured.json` need a real T4 run.
- Spike not yet checked on a Vercel preview (verified locally in Firefox only).

## Phase 0 results from running Gpubox 1.0.0 (Node, A100 profile, raceDetection on)

### 0.3.3 Counter fields (`sim.getCounters().toJSON()`)
`threadsLaunched, blocksLaunched, globalLoads, globalStores, globalLoadBytes, globalStoreBytes, totalBytesRead, totalBytesWritten, globalTransactions, coalescedTransactions, dramReadBytes, dramWriteBytes, sharedLoads, sharedStores, sharedLoadBytes, sharedStoreBytes, bankConflicts, syncthreadsCount, divergentBranches, atomicOps, atomicMaxContention, memcpyH2DBytes, memcpyD2HBytes, crossGpuBytes, ncclOps, flopCount, estimatedCycles, estimatedTimeMs, computeUtilization, memoryUtilization, occupancy`. `getDiagnostics()` returns an array (empty on clean runs).

### Metric gaps found on Gpubox 1.0.0 (all fixed, see the section below)
| Observed | Kernel | Problem |
|---|---|---|
| `divergentBranches = 0` | `if (i%2==0) ... else ...` | Obvious intra-warp divergence not counted |
| `coalescedTransactions == globalTransactions` always | naive 64x64 transpose | No coalescing efficiency signal; uncoalesced writes not distinguished |
| `flopCount = 0` | saxpy, tiled matmul | FLOPs only counted for atomics (1024 for the histogram); roofline needs this |
| `bankConflicts = 262144` | tiled matmul (As[ty][k], Bs[k][tx]) | Expected ~0 (broadcast and unit-stride); likely a false positive |
| Transpile error | `atomicAdd(&h[d[i]%16], 1)` | `&` on an indexed expression inside a call fails; `int b=...; atomicAdd(&h[b],1)` works |
Until these are fixed, `lowerBound` can rely on `globalLoadBytes/StoreBytes`, `sharedLoadBytes`, `syncthreadsCount`, `atomicOps`, `estimatedTimeMs`. Divergence, coalescing, FLOPs and bank-conflict claims need model-only visualizations or Gpubox fixes first.

### 0.3.7 Timing profile (ms, single run, Node)
| Kernel | create | compile | build fn | execute | counters |
|---|---|---|---|---|---|
| saxpy 4096 | 0.7 | 12.9 (cold) | 0.06 | 53.7 | 0.4 |
| transpose 64x64 | 0.1 | 2.2 | 0.07 | 35.6 | 0.03 |
| divergent 1024 | 0.1 | 1.4 | 0.11 | 7.8 | 0.14 |
| histogram 1024 | 0.1 | 1.6 | 0.12 | 9.9 | 0.06 |
| tiled matmul 64x64 | 0.1 | 2.0 | 0.11 | 445 | 0.03 |
Hypothesis confirmed: execution dominates (up to 200x parse). The compile cache is worthwhile only for the cold first compile; keep test sizes small (matmul 64x64 already costs ~0.45 s per case). Browser WASM load time is still unmeasured (needs the spike page).

### 0.3.2 Security
`docs/SECURITY_AND_CSP.md` confirms JS engine needs `unsafe-eval` (`new Function`); the WASM engine needs only `wasm-unsafe-eval`. Plan stands: run learner code in a sandboxed Worker on a separate origin, hard timeout, grant `unsafe-eval` only there. Built-in watchdog defaults: 50,000 steps, 2,000 ms.

## Gpubox fixes made (patches in `docs/cuda/gpubox-patches/`, to apply to `aadityansha06/Gpu-Box`)
- Divergence is now measured: the transpiler rewrites `if (c)` to record each lane's outcome; a warp-level branch event is divergent when lanes disagree (`divergentBranches`, new `branchEvents`).
- Coalescing: new `idealGlobalTransactions` and `coalescingEfficiency`; `coalescedTransactions` now means the ideal count. Naive 64x64 transpose measures 0.4.
- FLOPs: `flopCount` is a static estimate (arithmetic operators in float statements, charged per executed statement). saxpy = 2N and tiled matmul = 2N^3 verified. Integer index math is excluded heuristically, so treat it as an estimate.
- Bank conflicts: counted per warp access (distinct words per bank; same-word broadcast is free) and flushed when the whole block reaches the barrier, not per thread. `t[x][0]` on `[32][32]` gives 31 replays, `[32][33]` gives 0, tiled matmul gives 0.
- Atomics: `atomicAdd(&h[d[i]%16], 1)` and `atomicAdd(h+(d[i]%16), 1)` now transpile.
- Workers: the runtime exported globals only to `window`, so it never loaded in a Web Worker; it now uses `globalThis`.
- T4 profile added (Turing, 40 SMs, 320 GB/s, 8.1 TFLOPS FP32, 4 MB L2).
- Caveat: `syncthreadsCount` counts per thread (64x64 matmul reports 32768), so the certificate must not treat it as a barrier count.
- Regression test `test-course-metrics.js`: 11 checks pass. Gpubox's own suite is unchanged at 169/175, same as before the changes.

## Spike results (Firefox headless, local static build of `/cuda/spike`)
Worker load 38 ms; first vecAdd (N=1000) 61 ms wall (compile 35, execute 22); output correct; compile-cache hit on rerun about 0.01 ms.

## CUDA problem bank (49 problems) and IDE integration

- Source: `cuda_kernel_engineering_handbook.md`. Every problem in it is in `data/cuda/problems/<NN-slug>/` as `meta.json`, `statement.md`, `starter.cu`, `solution.cu`, `explanation.md` (the handbook text for that problem), `harness.js`. The handbook said 45 problems in its intro but contains 49 (CU-001..CU-052 minus 041-043); all 49 are included. CU-052's handbook entry was truncated, so the capstone is defined here as a two-kernel MLP block.
- Statements and harnesses are new text; only `explanation.md` is the handbook's own prose. `externalRef` keeps the source list numbers as metadata.
- Run path: IDE page -> `UnifiedExecutor` (language `cuda`) -> `processes/code-execution/cuda-service.ts` -> Web Worker `platform/static/gpubox/worker.js` -> pinned Gpubox in `platform/static/gpubox/1.0.0-tt2/`. Run checks the first two visible cases; Submit runs all cases including hidden ones, checks simulator diagnostics (race, out-of-bounds, divergent barrier, NCCL order) and the efficiency checks some problems define (transpose coalescing, tiled-matmul reuse, float4 loads, warp shuffle without shared memory).
- Two problem modes: `kernel` (harness launches the learner's kernels and compares buffers) and `program` (CU-047 and CU-051: a whole multi-GPU host program, judged by its output and by the simulator's collective checks).
- Tests: `processes/cuda/problems.spec.ts` runs every reference solution and every starter through the same worker file the browser loads. Reference passes all cases; starter must not.
- Known limits of the simulator model: memory is float32, so integers are exact below 2^24; atomicMax/Min/CAS use an integer view and are not used by any problem; templates and structs are not supported by the transpiler, so problems avoid them (CU-016 uses two shared arrays instead of a `Pair` struct); timings are a model; dropout hashes must keep products below 2^53.

## Additional Gpubox fixes for the problem bank (patches 0003 to 0006)
Integer division and `(int)` casts follow C++ semantics; `u`/`ull` literal suffixes, `constexpr`, `__forceinline__`, `erff`, `CUDART_INF_F`; `float4` loads and stores (one 16-byte access, alignment checked, `P + offset` form); dynamic `extern __shared__` arrays take the launch's size; atomics on static `__shared__` arrays (bypassing the race detector); `__shared__ unsigned` arrays; NCCL per-rank collectives are checked for matching kind, count, type, root and order as they arrive.

## Round 2 (feedback on the first version)
- Statements: LaTeX for formulas; the kernel signature is plain text (class `cuda-signature`, 3.5 px larger than the prose), not a code box.
- The IDE editor label, solution tabs and status bar say CUDA C++, never Python. `starterFor('cuda')` now returns the problem's starter, so a fresh editor opens on the kernel signature(s) with an empty body (before this the editor opened empty unless code was already saved).
- Compile errors: `lintSource` in the worker reports unbalanced brackets, an unclosed comment or string, and a missing `;` with the line and a code frame ("Compile error (line 4): This line does not end with ';' ..."). Undeclared names report the line they first appear on. The IDE labels it "CUDA compile error". `problems.spec.ts` checks every reference and starter for false positives.
- Solution tab: a "Memory-bound or compute-bound?" section is written from measured numbers (`data/cuda/problems/*/metrics.json`, produced by `npm run cuda:metrics`; the spec fails if a file is stale). It gives bytes, FLOPs, arithmetic intensity, the A100 ridge point, and shared-memory/coalescing/divergence facts. Multi-GPU problems get a cluster report instead.
- Report additions: per-bank shared-memory strip plus bank-conflict heat (Gpubox patch 0007 adds `bankAccesses`/`bankReplays`), and for multi-GPU programs a per-GPU collective and interconnect-bytes summary. These are text in the Console/Tests output, not graphical panels.
- Four new multi-GPU problems: CU-053 Broadcast, CU-054 AllGather, CU-055 ReduceScatter, CU-056 data-parallel gradient averaging (a kernel plus AllReduce). They are not in the handbook, so their explanations are written here.
- Navbar: CUDA replaces Problemset (`/problemset` still works by URL). `/cuda` is a landing page with progress and a Continue button; `/cuda/problems` has the same filter bar as the DSA sheet (search, topic, difficulty, status) and per-stage progress.

## Known test note
`e2e/build-output.spec.ts` ("client JavaScript stays inside its size budget") only runs when a `build/` exists. It already fails on the base branch: a build of the unmodified branch has 3.62 MB of client JS against the 2.5 MB budget (this branch's own app code adds about 17 KB). The pinned simulator engine under `/gpubox/` (about 380 KB) is exempted like `/vendor/` so it does not add to that total. The budget itself is untouched.
