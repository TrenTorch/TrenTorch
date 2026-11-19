# Debugging and the profiling mindset

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

## Interactive: Annotated report

<div class="cuda-viz" data-viz="VIZ-ANNOTATED-REPORT" data-title="Annotated report" data-spec="VIZ-ANNOTATED-REPORT"></div>

## A checklist of numbers to read from any report

| Number | Healthy | Suspicious | Chapter |
|---|---|---|---|
| Global load efficiency | ~100% | < 50% | D1 |
| Bytes moved ÷ lower bound | ≈ 1-1.3 | > 2 | D2 |
| Bank-conflict cycles | 0 | > 0 on hot loops | D5 |
| Lane utilization / divergence | ~100% | < 70% in the main loop | C1 |
| Occupancy & limiter | matches the kernel's latency needs | limiter = registers with spills | B4, D6 |
| % of roofline | > 70% | < 30% | D2 |
| Register spills | 0 | > 0 | D6 |

## Compute-sanitizer family

`memcheck` (out-of-bounds, misaligned access, leaks), `racecheck` (shared-memory hazards RAW/WAR/WAW), `synccheck` (barrier misuse, divergent `__syncthreads`), `initcheck` (reads of uninitialized global memory). The simulator's four diagnostic classes correspond one-to-one.

## Determinism checklist

Run the same input 10 times: results must be bitwise-identical unless you intentionally use atomics/unordered reductions. If they differ: (1) race, (2) uninitialized memory, (3) float atomics ordering, (4) `__syncthreads()` missing, (5) out-of-bounds read of a neighbouring allocation.

## Timing correctly

Use CUDA events (`cudaEventRecord` before/after, `cudaEventElapsedTime`), **warm up** (first launch includes context/JIT costs), run ≥ 10 iterations, report the **median**, and synchronize before stopping the clock (A2/B5). Compare against the copy-kernel bandwidth (A4) for memory-bound kernels.

## Check yourself

1. A kernel gives different results on repeated runs. Name two likely causes.
2. Your report says 1,024 bytes moved per 128 useful. What is the efficiency and which chapter helps?
3. A kernel's global load efficiency is 25% and its bank conflicts are zero. Which chapter do you open first?
4. Why must you warm up before timing?

<details class="answers">
<summary>Show answers</summary>

1. race, uninitialized memory/atomic ordering.
2. 12.5% ⇒ D1.
3. D1.
4. first launch includes context/JIT setup.

</details>

## Practice

[CU-048](problem:CU-048) · [CU-049](problem:CU-049) · [CU-050](problem:CU-050) · [CU-051](problem:CU-051)

*PMPP reference:* Ch. 6 (performance checklist and tuning strategies), Ch. 22 (profiling and tooling context).
