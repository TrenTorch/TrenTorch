# float vs float4 (vectorized access)

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

## Interactive: Does wider help?

<div class="cuda-viz" data-viz="VIZ-FLOAT4-BANDWIDTH" data-title="Does wider help?" data-spec="VIZ-FLOAT4-BANDWIDTH"></div>

## Bytes in flight, quantified

One warp issuing `float` loads has 32 × 4 = 128 B in flight per load instruction; with `float4` it is 512 B. For the T4 case from A5 (25 × 128 B loads per SM needed):
- `float` loads: need 25 *independent* warp loads outstanding per SM.
- `float4` loads: need ≈ 7 (3.2 KB ÷ 512 B).
With 32 resident warps per SM (the T4 maximum, *(approx.)*), plain `float` already has enough if each warp keeps one load outstanding; **the advantage appears when occupancy is low or each warp serializes load → use → load.** Using `float4` is a cheap form of ILP.

## Instruction counts

For N = 2²⁶ elements: scalar needs N/32 = 2,097,152 warp-level load instructions; `float4` needs N/128 = 524,288. The kernel moves the same bytes; the saving is in issue slots, address arithmetic and L1 pressure.

## Tails with alignment

For N not divisible by 4: `N4 = N / 4` vector elements and `rem = N % 4` tail elements (0-3). N = 10,000,001 → 2,500,000 float4 + 1 tail. Use `(N4 + B - 1) / B` blocks for the vector part, and let the last few threads (or one extra thread) handle the tail with scalar code.

## Check yourself

1. Why can a `float4` load fault if the pointer is offset by 4 bytes?
2. N = 1,000,003. How many `float4` elements and how many tail elements?
3. Would `float4` help a kernel that is compute-bound?
4. N = 10,000,001, block 256: blocks for the float4 part?
5. Why can `float4` give *no* speed-up if the scalar kernel already reaches 85% of peak bandwidth?

<details class="answers">
<summary>Show answers</summary>

1. misaligned vector access faults.
2. N = 1,000,003 ⇒ 250,000 float4 elements + 3 tail elements.
3. no.
4. ⌈2,500,000/256⌉ = 9,766.
5. already near the ceiling.

</details>

## Practice

[CU-012 ReLU with float4](problem:CU-012)

*PMPP reference:* Ch. 6 (memory-bound kernels, coalescing, thread coarsening), Ch. 5 (memory scope).
