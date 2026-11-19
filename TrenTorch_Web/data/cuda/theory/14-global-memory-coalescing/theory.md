# Global memory coalescing

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

## Interactive: From 32 addresses to transactions

<div class="cuda-viz" data-viz="VIZ-COALESCING" data-title="From 32 addresses to transactions" data-spec="VIZ-COALESCING"></div>

## A general transaction formula

For one warp load, let *A* be the set of 32 byte-addresses and each access `w` bytes wide. Sectors fetched = number of distinct 32-byte-aligned sectors touched by any byte of any access.
$$\text{efficiency} = \frac{32 \cdot w}{32 \cdot \text{sectors}} = \frac{w \cdot 32}{\text{sectors} \times 32}$$
Stride-*s* float access (w = 4):
| Stride s (floats) | Span (bytes) | Sectors | Efficiency |
|---|---|---|---|
| 1 | 128 | 4 | 100% |
| 2 | 256 | 8 | 50% |
| 4 | 512 | 16 | 25% |
| 8 or more | ≥ 1,024 | 32 (one per lane) | 12.5% |
Efficiency never drops below 12.5% for 4-byte elements, because each lane costs at least one 32-byte sector. For 16-byte (`float4`) accesses the floor is 50%.

## Effective bandwidth under a bad pattern

A stride-4 kernel at 25% efficiency can use at most 0.25 × (η × 2,039 GB/s) ≈ **430 GB/s of useful data** on an A100 even though the memory system is saturated. Reports should print both "bytes moved" and "useful bytes".

## The transpose, quantitatively

Naive transpose of an N × N float matrix: reads coalesced, writes strided by N. Reads use 100% of their sectors; writes use 12.5%. Ideal traffic = 4N² (read) + 4N² (write) = 8N² bytes. Actual = 4N² (read at 100%) + 4N² ÷ 0.125 = 32N² (write at 12.5%) = 36N² bytes, so **4.5× more traffic than necessary**. The shared-memory tiled version (D4/D5) restores both sides to 100% and approaches the copy-kernel bandwidth.

## Check yourself

1. A kernel reads `in[threadIdx.x * 16]` (floats). Efficiency?
2. Why does swapping `x` and `y` in a 2D kernel make it slower even though the result is identical?
3. Why does AoS hurt when you only read one field?
4. What is the lowest efficiency a 4-byte-element warp load can have?
5. Naive transpose moves how many times the ideal bytes?
6. Float4 access with stride 2 (in float4 units): efficiency?

<details class="answers">
<summary>Show answers</summary>

1. 12.5%.
2. the warp walks down a column ⇒ strided.
3. fields interleaved ⇒ strided reads.
4. 12.5%.
5. 4.5×.
6. 50%.

</details>

## Pitfalls

- Column-wise access in a row-major array.
- Misaligned base pointers (rare with `cudaMalloc`, common with offset sub-arrays).

## Practice

[CU-009 Matrix Addition](problem:CU-009) · [CU-030 Matrix Transpose](problem:CU-030)

*PMPP reference:* Ch. 6 (memory coalescing, corner turning, thread coarsening), Ch. 3/5 (row-major layout).

## Further reading

- NVIDIA CUDA C++ Programming Guide and Best Practices Guide; NCCL documentation
