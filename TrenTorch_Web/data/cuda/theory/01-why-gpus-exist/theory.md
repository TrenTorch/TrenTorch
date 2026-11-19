# Why GPUs exist

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

## Interactive: Two kinds of processor

<div class="cuda-viz" data-viz="VIZ-CPU-VS-GPU" data-title="Two kinds of processor" data-spec="VIZ-CPU-VS-GPU"></div>

## Latency versus throughput as numbers

CPU vs GPU is not "fast vs slow", it is a different point on a **latency-throughput trade-off**. Little's law again: *work in flight = throughput × latency*. A CPU core keeps few operations in flight with very low latency; a GPU keeps tens of thousands in flight and tolerates 400+ cycle latency per operation.

| Quantity *(approx., server class)* | CPU | GPU (A100) |
|---|---|---|
| Hardware threads | ~100 | 108 SMs × 2,048 = 221,184 resident |
| Peak FP32 | ~2-4 TFLOPS (AVX-512) | 19.5 TFLOPS |
| DRAM bandwidth | ~50-100 GB/s | ~2,039 GB/s |
| **FLOP per byte (machine balance)** | ~30-60 | **9.6** |
| Cache per thread | MBs | ~tens of bytes |

A GPU's *machine balance* is lower than you would guess, which is why even moderately arithmetic kernels (AI in the tens) become compute-bound on it, and why memory-bound kernels (AI < 1) are the norm in deep learning outside big matmuls.

## Work, span, and why dependency chains hurt

Model a computation as a graph. **Work** *W* = total operations; **span** *S* = longest chain of dependent operations. Ideal parallel time on *p* processors satisfies
$$T_p \ge \max\!\Big(\frac{W}{p},\; S\Big)$$
- Adding two arrays of N numbers: W = N, S = 1. Parallelism = W/S = N.
- Summing N numbers: W = N − 1, S = log₂N (with a tree). Parallelism ≈ N / log₂N.
- Fibonacci recurrence: W = N, S = N. Parallelism ≈ 1, so a GPU cannot help.

This W/S view is how you judge a problem before touching code, and it returns in chapters E2 (reduction), E6 (scan: work-efficient vs depth-efficient) and E8 (sorting).

## Interactive: How parallel is this problem?

<div class="cuda-viz" data-viz="VIZ-WORK-SPAN" data-title="How parallel is this problem?" data-spec="VIZ-WORK-SPAN"></div>

<div class="cuda-diagram" data-diagram="gpu-data-flow" data-title="Follow one launch from host to thread"></div>

## Check yourself

1. A job adds two arrays of 10 million floats. CPU or GPU? Why?
2. A job computes the next Fibonacci number from the previous two, a million times in a row. CPU or GPU? Why?
3. True or false: a GPU thread is faster than a CPU thread.
4. A computation has W = 10⁹ and S = 10⁴. What is the maximum useful number of processors?
5. Why does the machine balance of a GPU make arithmetic intensity so important?

<details class="answers">
<summary>Show answers</summary>

1. GPU: independent elementwise work... *but* if data starts on the host and is used once, A5's worked example 2 shows PCIe makes the GPU slower than the CPU; the GPU wins only if data stays resident or many passes follow.
2. CPU: span = N (dependency chain).
3. False: each GPU thread is slower; the GPU wins through massive parallelism. *Additional:*
4. W/S = 10⁵.
5. low machine balance: small AI ⇒ memory-bound.

</details>

## Pitfalls

- Assuming "more cores" always means faster. The workload must have enough independent work to keep them busy.

*PMPP reference:* Ch. 1 (motivation, CPU vs GPU design goals), Ch. 19 (computational thinking: choosing parallelizable formulations).
