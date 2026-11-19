# Numerical precision and mixed precision

## Why precision is a performance topic

Halving the bytes per element **doubles** memory-bound throughput; tensor cores run 8-16× faster than FP32 cores on lower precision. But fewer mantissa bits mean larger rounding error and a narrower range.

## The formats *(spec)*

| Format | Layout (sign/exp/mantissa) | Unit roundoff u | Max finite | Typical use |
|---|---|---|---|---|
| FP32 | 1 / 8 / 23 | 2⁻²⁴ ≈ 6.0×10⁻⁸ | 3.4×10³⁸ | default compute, accumulators |
| TF32 | 1 / 8 / 10 (19 bits used) | 2⁻¹¹ ≈ 4.9×10⁻⁴ | 3.4×10³⁸ | tensor-core matmul inputs |
| FP16 | 1 / 5 / 10 | 2⁻¹¹ ≈ 4.9×10⁻⁴ | **65,504** | inference, training with loss scaling |
| BF16 | 1 / 8 / 7 | 2⁻⁸ ≈ 3.9×10⁻³ | 3.4×10³⁸ | training (FP32-like range) |
| FP8 E4M3 | 1 / 4 / 3 | 2⁻⁴ = 0.0625 | 448 | inference/training with scaling |
| FP8 E5M2 | 1 / 5 / 2 | 2⁻³ = 0.125 | 57,344 | gradients |
Rule: **range** (exponent bits) decides overflow/underflow; **precision** (mantissa bits) decides rounding error.

## Mixed precision: what to keep in FP32

- **Accumulators.** A dot product of K terms in FP16 accumulating in FP16 has error growing ~K·u; tensor cores accumulate in FP32 (or higher) so error depends on the *input* rounding only.
- **Reductions** across many elements (sums, norms, softmax denominators, losses).
- **Master weights** in training (updates of 10⁻⁵ relative size vanish if added to FP16 weights; u = 4.9×10⁻⁴).
- **Exponentials**: in FP16, e^x overflows for x > 11.09 (e¹² = 162,755 > 65,504), which is another reason softmax subtracts the row max (E3).

## Loss scaling (FP16 training)

Gradients are small; many fall below FP16's smallest normal (≈ 6.1×10⁻⁵) and flush to zero. Multiply the loss by a scale S (e.g., 1,024) before backward, divide gradients by S afterwards; reduce S when overflow occurs. BF16 has FP32's range so it generally needs no scaling.

## Bytes, not just FLOPs

Switching a memory-bound elementwise kernel from FP32 to FP16 halves bytes ⇒ ~2× faster in the time model of A5 (N = 2²⁶ ReLU: 0.31 ms → 0.16 ms on an A100). A matmul switching to FP16 tensor cores moves from the FP32 roof (19.5) to 312 TFLOPS, which pushes the ridge to ≈ 153 FLOP/B (D2).

## Error you can compute

Single FP16 rounding: relative error ≤ u = 4.9×10⁻⁴; product of two FP16 numbers computed exactly then rounded: ≤ u; sum of K FP16 terms accumulated in FP16: worst case ≈ K·u (with K = 1,024 that is ~0.5, so useless), accumulated in FP32: ≈ u + K·6×10⁻⁸ (6×10⁻⁵ for K = 1,024).

## Interactive: Same sum, four formats

<div class="cuda-viz" data-viz="VIZ-PRECISION-LADDER" data-title="Same sum, four formats" data-spec="VIZ-PRECISION-LADDER"></div>

## Check yourself

1. Why does an FP16 running sum of ones stop at 2,048?
2. At what logit value does FP16 `exp` overflow?
3. Why do mixed-precision matmuls keep FP32 accumulators?

<details class="answers">
<summary>Show answers</summary>

1. spacing between FP16 numbers reaches 2 above 2,048, so +1 rounds back.
2. x ≈ 11.09 (e¹² overflows).
3. rounding error grows ~K·u otherwise.

</details>

## Proposed problem

<div class="coming-soon"><div class="cs-head"><strong>CU-056 Mixed-precision dot product</strong><span class="cs-badge">Coming soon</span></div><p>FP16 inputs, FP32 accumulator; compare against FP16-only accumulation; report shows bytes saved and max error.</p></div>

*PMPP reference:* Ch. 6 (numerical considerations: floating-point precision, accuracy and the non-associativity of summation in the performance chapter; reduction order discussion in Ch. 10), Ch. 22 (reduced precision and future evolution). **Not in PMPP's main text:** BF16/TF32/FP8 details, loss scaling: cite vendor docs and the mixed-precision-training literature.

## Further reading

- Micikevicius et al., "Mixed Precision Training" (2018)
