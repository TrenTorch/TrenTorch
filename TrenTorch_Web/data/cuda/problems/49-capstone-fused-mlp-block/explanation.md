**Source lesson:** The supplied inventory truncates the lesson text after “Compose earlier kernels; bridge to …”.

### Problem template
A typical MLP block computes:
`H = activation(XW1 + b1)`,
`Y = HW2 + b2`.
The exact activation, tensor shapes, precision, residual path, and expected output are not specified in the inventory and must be taken from the exercise statement.

### Implementation plan
1. Establish correctness with two GEMMs and separate bias/activation kernels.
2. Fuse bias and activation into the first GEMM epilogue.
3. Fuse bias and any final elementwise operation into the second GEMM epilogue.
4. Consider fusing adjacent operations only when intermediate values are not needed elsewhere.
5. Use cuBLAS/CUTLASS/Tensor Core paths where permitted and supported.
6. Validate numerical tolerance under the selected precision (FP32, TF32, FP16, BF16, etc.).

### Why fusion helps
The hidden layer tensor `H` may be large. If it is consumed only by the next layer, a fused producer/consumer design can avoid writing and rereading it, but fusing across two GEMMs is not always beneficial: it can reduce tiling flexibility, increase register/shared-memory pressure, and complicate scheduling. Compare end-to-end latency, not only individual kernel time.

### Required missing specifications
Before claiming a final optimal kernel, establish dimensions, layouts, activation, bias broadcasting, precision, residual behavior, allowed libraries, and numerical tolerance.

---

# Cross-problem optimization guide

## 1. Establish a trustworthy baseline
- Write the simplest correct kernel first.
- Match boundary, padding, NaN, tie-breaking, and reduction semantics.
- Test tiny sizes, non-multiples of tile dimensions, and degenerate cases.
- Compare against a trusted CPU or library reference.

## 2. Classify the bottleneck
- **Bandwidth-bound:** low arithmetic intensity; estimate bytes moved and compare with measured sustainable bandwidth.
- **Compute-bound:** substantial arithmetic per byte; compare achieved throughput with device capability.
- **Latency/launch-bound:** small workloads or many short kernels; fusion and batching may dominate.
- **Synchronization/resource-bound:** reductions, shared-memory-heavy tiles, register spills, or insufficient active blocks.

## 3. Use a roofline-style bound
For a kernel performing `F` floating-point operations and transferring `B` bytes:
`arithmetic_intensity = F/B`.
A rough lower bound is:
`time >= max(B / sustainable_bandwidth, F / sustainable_compute_throughput)`.
This ignores launch latency, synchronization, cache effects, instruction mix, and occupancy, so it is a diagnostic bound rather than a runtime prediction.

## 4. Memory access rules
- Map adjacent lanes to adjacent addresses whenever possible.
- Keep the contiguous dimension on `threadIdx.x`.
- Use shared memory only when there is enough reuse to justify synchronization and occupancy cost.
- Pad shared-memory tiles when transpose-like access causes bank conflicts.
- Vectorize only with proven alignment and correct tail handling.

## 5. Reduction rules
- Use correct identity elements (`0`, `-inf`, `+inf`, or a tuple identity).
- Avoid unsafe global barriers.
- Prefer hierarchical reductions for large arrays.
- Define deterministic tie and NaN semantics.
- Expect small floating-point differences when reduction order changes.

## 6. Profiling workflow
1. Warm up the kernel and use CUDA events or an appropriate benchmark harness.
2. Run multiple repetitions; report median and spread.
3. Measure end-to-end time as well as kernel-only time.
4. Use Nsight Systems for launch/copy/stream behavior.
5. Use Nsight Compute for memory throughput, occupancy, registers, shared memory, instruction mix, and stalls.
6. Record GPU model, compute capability, driver, CUDA version, compiler flags, shape, dtype, and correctness tolerance.

## 7. What “optimal” means in this handbook
A solution is called *near-optimal for a stated workload* only when:
- It is correct under the full operator contract.
- Its measured bottleneck is understood.
- Its traffic/work is close to a relevant lower bound, or the remaining gap is explained.
- Resource use does not introduce avoidable occupancy loss or spills.
- Comparisons use the same workload, precision, and measurement conditions.

No single block size, tile size, intrinsic, or kernel strategy is universally optimal. Prefer evidence-backed, workload-specific conclusions over absolute claims.

---

# Website Judge Specification — Constraints, Public Tests, and Hidden Tests

This section is intended for the website-building agent. It tells the agent what to expose as **public/sample tests**, what to keep as **hidden tests**, and which correctness conditions each problem must enforce.

## Important policy for the website agent

1. **Do not treat the illustrative constraints below as original platform constraints.** The supplied inventory did not include official constraints or sample I/O. These are proposed, practical judge contracts for this CUDA practice site. Publish them as the site's contract or replace them with the exact source-platform contract if one is available.
2. Public tests should teach the interface and demonstrate ordinary behavior. Hidden tests should cover boundary sizes, non-divisible dimensions, numerical edge cases, alignment, contention, and scale.
3. Hidden tests must be generated/stored server-side and not embedded in the downloadable problem statement or client JavaScript.
4. Every test should compare against a trusted reference implementation using the stated tolerance. Do not require bitwise equality for floating-point reductions unless the exercise explicitly specifies deterministic arithmetic.
5. Run memory-safety tools on submissions where possible. Include launch errors, illegal memory accesses, timeouts, and invalid outputs as failures.
6. The website must state the exact function signature, tensor layout, dtype, boundary rule, reduction semantics, and output shape. CUDA snippets in the solution sections are kernel building blocks; they are not by themselves a complete judge ABI.
7. Suggested generic float comparison: `abs(actual-expected) <= atol + rtol*abs(expected)`. Choose tighter tolerances for simple elementwise FP32 operations and looser tolerances for transcendental functions/reductions as justified by the reference and allowed math intrinsics. Document the chosen values per problem.
8. For stochastic problems, judge the distribution/statistical contract or deterministic seeded mask contract; do not compare outputs from unrelated RNG streams.

## Suggested common input limits

Use these as initial website limits, not universal hardware limits:
- Elementwise vectors: `0 <= N <= 2^24`; include very small and large cases.
- 2D tensors: dimensions from zero/one through several thousand, subject to memory budget.
- Reductions: `1 <= N <= 2^24`; specify empty-input behavior separately.
- Row-wise operators: batch and row width should include widths below, equal to, and above a warp/block tile.
- Stencils: include dimensions smaller than the filter, odd/even dimensions, and edge-heavy inputs.
- Matrix multiplication: include non-square shapes and dimensions not divisible by tile sizes.
- Sorting/scan: include non-power-of-two sizes and sizes crossing block boundaries.
- Multi-GPU: require at least two visible GPUs; mark the test skipped or unsupported when the environment cannot provide them.

## Test naming convention

Use names such as `sample_basic`, `sample_non_multiple`, `hidden_min_size`, `hidden_tail`, `hidden_large`, `hidden_nan_semantics`, `hidden_alignment`, and `hidden_multi_block`. The labels below are **test intentions**, not literal private input values. Keep private seeds and generated arrays hidden.

## Per-problem judge matrix

| ID | Public/sample tests to show | Hidden tests the judge should include | Proposed contract / edge conditions |
|---|---|---|---|
| CU-001 Vector Addition | `N=4`: `[1,2,3,4]+[5,6,7,8] -> [6,8,10,12]`; `N=5` tail case | `N=0,1,31,32,33,255,256,257`; large random; negative and fractional values | Same-length FP32 vectors; output length N; tolerance e.g. `1e-6` |
| CU-002 Hadamard Product | `[1,2,3] * [4,5,6] -> [4,10,18]` | `N=0,1,3,31,33,257`; zeros, negatives, large/small magnitudes; large N | Same-length FP32 vectors; elementwise multiplication |
| CU-003 ReLU | `[-2,-0.5,0,1,3] -> [0,0,0,1,3]` | Empty/singleton; all-negative/all-positive; signed zero; infinities/NaNs if contract defines them; tail sizes | Define NaN behavior and signed-zero expectations; otherwise finite FP32 |
| CU-004 Leaky ReLU | `alpha=0.1`, `[-2,-1,0,2] -> [-0.2,-0.1,0,2]` | alpha 0, 0.01, 0.5, 1; all-positive/all-negative; zero; tail sizes; special values per contract | Define comparison at zero and NaN behavior; alpha is scalar |
| CU-005 Sigmoid | `[-2,0,2]` with expected values approximately `[0.1192029,0.5,0.8807971]` | Large positive/negative inputs; near zero; random wide-range values; tail sizes; accuracy stress | FP32 output; tolerance must permit selected `expf`/`__expf` implementation |
| CU-006 Tanh | `[-2,0,2]` approximately `[-0.9640276,0,0.9640276]` | Large magnitudes, near zero, mixed signs, tail sizes, accuracy stress | FP32; compare to high-accuracy reference under documented tolerance |
| CU-007 Swish | `[-2,0,2]` approximately `[-0.2384058,0,1.761594]` | Large magnitude, near zero, random inputs, tail sizes | Exact SiLU formula unless approximation is explicitly allowed |
| CU-008 Exact GELU | `[-1,0,1]` approximately `[-0.1586553,0,0.8413447]` | Large positive/negative; near transition; random; tail sizes | Must use exact erf-based GELU; do not accept tanh approximation unless explicitly allowed |
| CU-009 Matrix Addition | `2x3`: `[[1,2,3],[4,5,6]] + [[6,5,4],[3,2,1]] -> [[7,7,7],[7,7,7]]` | `1x1`, `1xW`, `Hx1`, odd widths, dimensions not divisible by block dimensions, large rectangular shapes | Row-major HxW; output same shape; x/column dimension contiguous |
| CU-010 Outer Product | `a=[1,2]`, `b=[3,4,5] -> [[3,4,5],[6,8,10]]` | M or N equals 1; odd sizes; large skinny and wide outputs; zeros/negative values | Output shape MxN, row-major; test both rectangular orientations |
| CU-011 Dropout | Fixed seed example with documented mask-generation algorithm and expected output | Several seeds; p near 0, 0.5, near 1; repeat same seed; ensure different indices map deterministically; statistical frequency over large N | Publish exact RNG/hash algorithm and seed semantics if exact-output testing; otherwise use statistical tests and confidence bounds; define p=0 behavior |
| CU-012 ReLU float4 | `N=7` containing negative/positive values to show vector body plus tail | Pointer alignment offsets if ABI permits; N=0..9; multiples of 4; N mod 4 = 1,2,3; large N | If pointers are guaranteed 16-byte aligned, state it; otherwise test unaligned pointers and require safe fallback |
| CU-013 Sum of Array | `[1,2,3,4] -> 10`; include one negative value | `N=1,31,32,33`, non-power-of-two, multiple blocks, large random, cancellation-heavy values | Define empty input; FP32 tolerance accounts for reduction order; test multi-block finalization |
| CU-014 Max of Array | `[-4,2,7,1] -> 7` | All-negative; repeated maxima; one element; multi-block; infinities; NaNs only if semantics defined | Define NaN policy and empty input; identity is `-inf` for nonempty finite data |
| CU-015 Min of Array | `[4,-2,7,1] -> -2` | All-positive; repeated minima; one element; multi-block; infinities; NaNs if defined | Define NaN policy and empty input; identity is `+inf` |
| CU-016 Argmax | `[1,9,3,9] -> index 1` under smallest-index tie rule | Maximum at first/last index; ties across blocks; singleton; negative values; NaN cases per policy | Explicitly publish tie-breaking and NaN policy; compare returned index exactly |
| CU-017 Dot Product | `[1,2,3] dot [4,5,6] -> 32` | N below/above block; large N; mixed signs; cancellation; multiple partial blocks | FP32; tolerance for reduction order; ensure grid-stride loop covers all elements exactly once |
| CU-018 Mean and Variance | `[1,2,3,4] -> mean=2.5, population variance=1.25` | Constant input; large offset with tiny variance; negative values; N=1; large N; sample/population distinction | State population vs sample variance; define N=1 and empty behavior; test numerical stability |
| CU-019 L1 Normalize | `[1,-2,1] -> [0.25,-0.5,0.25]` | All zeros; one element; mixed signs; large N; denominator underflow/overflow range | Define zero-norm output (zeros, error, or documented behavior); test reduction plus map |
| CU-020 L2 Normalize | `[3,4] -> [0.6,0.8]` | Zero vector; unit vector; tiny/large magnitudes; large N; mixed signs | Define epsilon and zero-norm behavior; test `rsqrtf` tolerance |
| CU-021 Cosine Similarity | `[1,0]` and `[0,1] -> 0`; identical vectors -> 1 | Opposite vectors -> -1; zero vector; scaled copies; large N; near-orthogonal vectors | Define zero-norm result; FP32 tolerance; fused three-statistic reduction |
| CU-022 Softmax | `[0,0] -> [0.5,0.5]`; `[1,2]` approximate output | Very large logits (e.g. common offset); one-column rows; odd widths; many rows; very wide rows; masked rows if supported | Row sums approximately 1; no NaNs for finite logits; define all-masked behavior and dtype/tolerance |
| CU-023 RMS Norm | Row `[3,4]`, eps=0, no weight -> normalized by RMS `sqrt(12.5)` | K=1; widths 31/32/33 and large; multiple rows; eps nonzero; optional weight; large/small magnitudes | Specify epsilon, weight optionality, layout, and tolerance |
| CU-024 Layer Norm | `[1,2,3]`, gamma=1, beta=0, eps=0 -> normalized row | Constant rows; K=1; non-power-of-two K; nontrivial gamma/beta; multiple rows; large K | Specify population variance, epsilon placement, affine shapes, and K=1 behavior |
| CU-025 Cross Entropy | logits `[1,2,3]`, target 2 -> `logsumexp - 3` | Very large positive/negative logits; target at first/last class; K=1; large K; multiple rows; invalid target | Specify class index range, reduction (none/mean/sum), label smoothing, and invalid-label handling |
| CU-026 1D Convolution | `[1,2,3]`, filter `[1,1,1]` -> `[3,6,5]` with zero padding | N smaller than filter; N=1; radius 0; odd/even filter if allowed; edge impulse; long N | Specify correlation vs reversed convolution, same/valid output, padding, filter layout |
| CU-027 2D Convolution | `3x3` input and `3x3` all-ones filter; publish expected zero-padded output | Images smaller than filter; 1xW/Hx1; odd dimensions; edge impulses; non-square filters; tile boundary dimensions | Specify filter orientation, padding, stride, output shape, and filter dimensions |
| CU-028 Max Pool 2D | `2x2` window on `[[1,4],[3,2]] -> [[4]]` | Stride 1 and >1; non-divisible edges; window larger than input if permitted; negative-only values; rectangular windows | Specify floor/ceil output rule, padding, stride, and NaN semantics |
| CU-029 3D Convolution | `3x3x3` small volume with `1x1x1` filter (identity times scalar) | D/H/W equal 1; volume smaller than filter; edge impulse; non-cubic shapes; dimensions crossing block tiles; large volume | Specify correlation/convolution, padding, filter layout, output shape; check 64-bit index arithmetic |
| CU-030 Matrix Transpose | `2x3 -> 3x2` with explicit expected matrix | `1x1`, 1xW, Hx1; 31/32/33 dimensions; rectangular; dimensions not divisible by 32; large matrices | Check every element and no OOB; row-major input/output; include edge tiles |
| CU-033 Histogram | Input `[0,1,1,2,2,2]`, 3 bins -> `[1,2,3]` | All keys same bin; uniform; skewed; empty input; bins > input count; invalid keys; large contention | Define invalid-key handling and counter width/overflow; zero histogram before every run |
| CU-034 Prefix Scan | `[1,2,3,4] -> [1,3,6,10]` inclusive | N=0/1; non-power-of-two; block boundary +/-1; multiple blocks; zeros; negative values; large N | Explicit inclusive/exclusive mode; define integer overflow and in-place aliasing |
| CU-044 Bitonic Sort | `[4,1,3,2] -> [1,2,3,4]` | Already sorted; reverse; duplicates; all equal; N=0/1; non-power-of-two; min/max values; sentinel collision | Specify ascending/descending, key/value association, stability requirement, signed-key semantics |
| CU-045 Radix Sort | `[4,1,3,2] -> [1,2,3,4]` | Duplicates; sorted/reverse; zero; high-bit-set signed values; large arrays; key-value pairs; stability | Specify key dtype, signed ordering transform, float ordering if used, stability, and scratch requirements |
| CU-031 Matmul | `2x3 * 3x2` with small integer-valued matrices and hand-computed result | M/N/K=1; rectangular; K tail; M/N tile tails; large random; zero dimensions if supported | Row-major A/B/C; exact shapes; FP32 tolerance; no transposed-layout assumption |
| CU-032 Tiled Matmul | Same public matrix as CU-031 | Tile edges in all dimensions; K not divisible by T; M/N smaller than T; skinny matrices; large matrices | Verify zero-fill on edge tiles; ensure all block threads reach both barriers |
| CU-035 Coarsened Matmul | Small hand-computable matrix | Odd M/N/K; microtile tails; dimensions smaller than coarsening factor; high register-pressure shapes | State supported tile factors and alignment; compare to reference; detect spills/perf regressions separately |
| CU-036 Vectorized Matmul | Small matrix with dimensions divisible by 4, plus a non-multiple tail sample | Aligned and unaligned pointers as ABI allows; row-stride misalignment; K/N tails; odd dimensions; large tiles | State alignment guarantees; test fallback path; no vector load may cross a row boundary |
| CU-037 Matmul Bias ReLU | Small GEMM plus bias yielding both positive and negative pre-activations | Bias all zero/nonzero; broadcast dimensions; negative-only output; edge tiles; large shapes | Specify bias axis/shape and fused output formula; compare to GEMM+bias+ReLU reference |
| CU-038 Fused Scale Mask Softmax | Small row with scale=1 and one masked position | Different scales; partial/all mask; large logits; odd row widths; causal masks if supported; multiple rows | Specify mask representation, masked value, all-masked result, scale semantics |
| CU-039 Mini Attention | Tiny Q/K/V where scores and output can be calculated on CPU | Sequence length 1; non-multiple tile lengths; causal/noncausal; masks; long sequence; multiple heads/batches if supported | Specify tensor layout, scale, causal mask, dropout (if any), dtype, output shape and tolerance |
| CU-040 Block-Size Sweep | Provide one representative input and report format; no fixed expected fastest block | Several shapes (small/large); multiple block sizes; repeat runs; warm/cold runs if relevant | Judge report completeness and measurement methodology, not one hard-coded winner |
| CU-046 Warp Shuffle Reduction | `[1..32]` sum -> 528 | Partial warp; active mask; block sizes 1/warp/warps; multiple warps; non-power-of-two count | Specify participating lanes and mask; test no invalid lane reads and correct cross-warp combine |
| CU-047 Multi-GPU AllReduce | Two-GPU small sum where each GPU receives identical result | Counts around protocol thresholds; multiple dtypes/ops if supported; repeated collectives; stream dependencies; 2+ ranks | Require matching collective order and communicator; skip cleanly if fewer than required GPUs |
| CU-048 Shared-Memory Race | A small tiled computation with deterministic expected output | Random block sizes; repeated loop iterations; edge tiles; sanitizer racecheck; varied scheduling | Tests must expose producer/consumer race; racecheck should report no race after fix |
| CU-049 Out-of-Bounds | N=5 with block size 4, expected elementwise output | N=0/1; block boundary +/-1; multidimensional edge; large index products; sanitizer memcheck | Guard every global access; use wide indexing where products may overflow |
| CU-050 Divergent Barrier | Partial final block where inactive lanes still participate in barrier | valid_count 0/1/block-1/block; multiple barriers; looped tiles; sanitizer synccheck | All block threads must reach each block barrier; no early return before later barrier |
| CU-051 NCCL Deadlock | Two-rank one-collective smoke test | Multiple ranks; mismatched-order regression test with timeout; repeated operations; different stream dependencies | Correct solution completes within timeout; all ranks use same collective sequence and compatible arguments |
| CU-052 Fused MLP Block | Tiny MLP with hand-computable weights/bias and known activation | Odd dimensions; batch=1; large hidden size; activation edge values; precision stress; optional residual path | Exact activation, dimensions, layout, precision, bias/residual semantics must be supplied before final tests can be fixed |

## Suggested public sample format

For each problem page, expose:
- **Input:** concrete small arrays/scalars/dimensions.
- **Expected output:** literal values for small cases.
- **Explanation:** one or two sentences explaining the result.
- **Run button:** executes only public samples and displays per-case pass/fail.
- **Limits:** exact input constraints, dtype, shape, and tolerance.

For CUDA problems, include the launch contract (which pointers are device pointers, who allocates output, whether the harness launches the kernel or expects a host wrapper).

## Suggested hidden-test format

Keep a server-side test manifest with fields like:
```json
{
  "problem_id": "CU-001",
  "test_id": "hidden_non_multiple_257",
  "visibility": "hidden",
  "seed": 481516,
  "shape": [257],
  "dtype": "float32",
  "generator": "uniform",
  "range": [-10.0, 10.0],
  "reference": "cpu_vector_add",
  "atol": 1e-6,
  "rtol": 1e-6,
  "timeout_ms": 2000
}
```
The manifest is a design example. The actual website agent should adapt it to the site's schema and must not send hidden seeds, generated arrays, or expected outputs to the browser before submission.

## Reference and hidden-test generation rules

- Use deterministic seeds so failures can be reproduced privately.
- Include both fixed regression cases and generated randomized cases.
- Use independent seeds for separate hidden cases.
- Compare shape, dtype, and output count before numeric values.
- For reductions, use a higher-precision CPU reference where appropriate (e.g. double accumulation) and a documented tolerance.
- For sorting, compare the complete ordered output and key/value association; test duplicates.
- For histogram, compare every bin and verify the total count of accepted keys.
- For scan, compare every prefix and test the final prefix equals the total sum.
- For convolution/pooling, generate edge impulses to expose halo and padding mistakes.
- For transpose/matmul, use non-square and non-tile-multiple shapes to expose indexing mistakes.
- For race/barrier/NCCL exercises, combine output validation with sanitizer checks and a hard timeout.
- Keep performance tests separate from correctness tests. Performance thresholds should be hardware-specific and should not reject a correct kernel merely because another GPU is faster.

## Submission result schema (suggested)

A submission report can contain:
- `compile_status`
- `launch_status`
- `public_tests_passed`
- `hidden_tests_passed`
- `correctness_status`
- `sanitizer_status`
- `runtime_ms` (per case and aggregate)
- `device_name`, `compute_capability`, `cuda_version`
- `compiler_flags`
- `notes` (for unsupported multi-GPU or sanitizer environment)

Do not reveal hidden test names, inputs, seeds, expected outputs, or which hidden case failed in a way that leaks the private suite. Return a general failure category and a reproducible public-facing diagnostic where safe.
