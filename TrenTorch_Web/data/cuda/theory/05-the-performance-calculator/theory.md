# The performance calculator

Every later chapter ends with a number. This chapter gives you the **eleven formulas** that produce those numbers, so you can predict a kernel's runtime *before* you write it, and know when a measurement is suspicious.

## Peak compute from the spec sheet

$$\text{Peak FP32 FLOP/s} = \text{SMs} \times \text{FP32 cores per SM} \times 2 \times f_{\text{clock}}$$
The factor 2 is because a fused multiply-add (FMA) counts as two floating-point operations.

- **T4:** 40 × 64 × 2 × 1.59 GHz ≈ **8.14 TFLOPS** *(boost clock)*.
- **A100:** 108 × 64 × 2 × 1.41 GHz ≈ **19.5 TFLOPS**.
- **H100 SXM:** 132 × 128 × 2 × ~1.98 GHz ≈ **67 TFLOPS**.

The vendor number assumes every core issues an FMA every cycle. Real kernels reach 70-90% on a good day.

## Peak bandwidth from the memory spec

$$\text{BW} = \frac{\text{bus width (bits)}}{8} \times \text{data rate per pin (Gbit/s)}$$
- **T4:** 256 bits ÷ 8 × 10 Gbit/s = **320 GB/s**.
- **A100 80 GB:** 5,120 bits ÷ 8 × ~3.19 Gbit/s ≈ **2,039 GB/s**.

**Achievable** bandwidth for a clean streaming kernel (a plain copy) is typically **80-90%** of this, written η ≈ 0.8-0.9. Always use η × peak for time predictions. Measure η yourself with a copy kernel (chapter D1).

## The ridge point and the roofline

$$\text{Ridge} = \frac{\text{Peak FLOP/s}}{\text{BW}} \quad [\text{FLOP/byte}]$$
$$\text{Attainable FLOP/s} = \min\big(\text{Peak},\; \text{AI} \times \text{BW}\big)$$

## The one-line time model

$$t \;\approx\; \max\!\left(\frac{\text{bytes}}{\eta_m \cdot \text{BW}},\; \frac{\text{FLOPs}}{\eta_c \cdot \text{Peak}}\right) + t_{\text{launch}}$$
`t_launch` is about **3-10 µs** per kernel launch on the host side *(approx.)*. For kernels that run for tens of microseconds it is not negligible (chapter F7).

## Worked example 1: ReLU on 2²⁸ floats (A100)

- N = 268,435,456. Bytes = 8N = 2.147 GB (read + write).
- Memory time at peak: 2.147 GB ÷ 2,039 GB/s = **1.05 ms**. At η = 0.85: **1.24 ms**.
- Compute time: N FLOPs ÷ 19.5 TFLOPS = **13.8 µs**.
- Ratio memory ÷ compute ≈ **75×**. The ALUs are idle > 98% of the time. No amount of arithmetic tuning matters.

## Worked example 2: why a single vector add should not go to the GPU

Setup: `c = a + b`, N elements, data starts on the host. CPU memory bandwidth 50 GB/s; PCIe 4.0 at 25 GB/s each way; A100 on-device 2,039 GB/s.
- CPU time: 12N bytes ÷ 50 GB/s = 2.4 × 10⁻¹⁰ · N s.
- GPU time = copy in (8N B) + copy out (4N B) over PCIe + kernel: 12N ÷ 25 GB/s + 12N ÷ 2,039 GB/s = (4.8 + 0.06) × 10⁻¹⁰ · N s.
- The GPU is about **2× slower for every N**, because the PCIe copy alone costs more than the CPU's entire computation.

Now run *k* kernels on data that stays resident: GPU = 4.8 × 10⁻¹⁰ N + k · 0.059 × 10⁻¹⁰ N vs CPU = k · 2.4 × 10⁻¹⁰ N. The GPU wins when k ≥ 2.05, so **at least 3 chained passes** over the same data. This is the quantitative reason for "keep data on the device" (chapter A2) and for kernel fusion (F3).

## Amdahl's law (and why "10,000 cores" is not "10,000×")

If a fraction *p* of the work is parallel and speeds up by *s*:
$$\text{Speedup} = \frac{1}{(1-p) + p/s}$$
p = 0.9 and s = 100 gives 1 ÷ (0.1 + 0.009) = **9.2×**; even with s → ∞ the ceiling is **10×**. The serial 10% (often the PCIe copy or a host loop) decides the result. **Gustafson's view:** if you can grow the problem with the machine, the serial fraction shrinks, which is why GPUs shine at large problems.

## Little's law for memory

$$\text{bytes in flight} = \text{latency} \times \text{bandwidth}$$
A T4 with 400 ns latency and 320 GB/s needs 128 KB in flight chip-wide: 3.2 KB per SM, or **25 128-byte warp loads outstanding per SM**. If your kernel has too few resident warps, or too few independent loads per warp, you cannot reach peak bandwidth (this is the reason for occupancy, B4, and vector loads, D3).

## Occupancy and wave arithmetic (preview)

$$\text{blocks per SM} = \min\!\Big(\Big\lfloor\tfrac{\text{threads}_{SM}}{B}\Big\rfloor,\ \Big\lfloor\tfrac{\text{regs}_{SM}}{B\cdot r}\Big\rfloor,\ \Big\lfloor\tfrac{\text{smem}_{SM}}{s}\Big\rfloor,\ \text{blocks}_{max}\Big)$$
$$\text{waves} = \Big\lceil \tfrac{\text{grid}}{\text{SMs} \times \text{blocks per SM}} \Big\rceil,\qquad \text{wave efficiency} = \frac{\text{grid}}{\text{waves} \times \text{SMs} \times \text{blocks per SM}}$$

## Transfer time with latency

$$t_{\text{copy}} = \alpha + \frac{D}{B_{\text{PCIe}}}, \qquad \alpha \approx 10\,\mu s$$
For small copies α dominates, so batch small transfers into one.

## Interactive: Predict before you run

<div class="cuda-viz" data-viz="VIZ-PERF-CALCULATOR" data-title="Predict before you run" data-spec="VIZ-PERF-CALCULATOR"></div>

## Check yourself

1. Compute the T4's peak bandwidth if the bus is 256 bits and the data rate is 14 Gbit/s.
2. For AI = 2 FLOP/B on the A100, what is attainable GFLOP/s?
3. Why is "ratio of memory time to compute time" a better diagnosis than "ratio of FLOPs to bytes" alone?

<details class="answers">
<summary>Show answers</summary>

1. 256/8 × 14 = 448 GB/s.
2. min(19.5 T, 2 × 2,039 G) = 4,078 GFLOP/s.
3. because the ratio of times directly says which resource limits runtime.

</details>

## Pitfalls

- Using peak instead of η × peak for predictions.
- Forgetting the PCIe terms when the data starts on the host.
- Counting an FMA as one FLOP when comparing with vendor TFLOPS.

## Further reading

- Williams, Waterman, Patterson, "Roofline: An Insightful Visual Performance Model" (2009)
