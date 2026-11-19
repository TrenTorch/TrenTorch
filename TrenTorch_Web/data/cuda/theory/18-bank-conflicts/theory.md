# Bank conflicts

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

## Interactive: 32 lanes, 32 banks

<div class="cuda-viz" data-viz="VIZ-BANK-GRID" data-title="32 lanes, 32 banks" data-spec="VIZ-BANK-GRID"></div>

## The general formula

For stride-*s* access `smem[s * lane]` on 4-byte words with 32 banks:
$$\text{conflict degree} = \gcd(s, 32)$$
| Stride s | gcd | Degree | Slowdown |
|---|---|---|---|
| 1 | 1 | none | 1× |
| 2 | 2 | 2-way | 2× |
| 3 | 1 | none | 1× |
| 4 | 4 | 4-way | 4× |
| 8 | 8 | 8-way | 8× |
| 16 | 16 | 16-way | 16× |
| 32 | 32 | 32-way | 32× |
| 33 | 1 | none | 1× |
Odd strides are conflict-free. That is exactly why padding a 32-wide row to 33 words works (column access has stride 33).

## 64-bit and wider accesses

For 8-byte (`double` / `float2`) accesses the hardware serves a half-warp per phase; the analysis uses 64-bit words with 16 effective banks per half-warp. Rule of thumb: stride-1 on any word size is conflict-free; for wider types verify with the profiler.

## Swizzling as an alternative to padding

Padding wastes `1/32` of the memory and breaks 16-byte alignment for vector loads. **XOR swizzling** stores element (r, c) at column `c ^ (r % 32)` so each row is permuted, keeping rows at power-of-two pitch. Conflict-free for both row and column access, and compatible with `float4`. (Used by high-performance GEMM kernels.)

## Scan's bank problem

Blelloch's strides double each level (E6): level *d* accesses `index·2^d`, giving up to 2^d-way conflicts. The standard fix: add `index >> 5` to every shared index (one pad word per 32).

## Interactive: Bank Stride Sweep

<div class="cuda-viz" data-viz="VIZ-BANK-GRID" data-mode="bank-stride-sweep" data-title="Bank Stride Sweep" data-spec="VIZ-BANK-STRIDE-SWEEP"></div>

## Check yourself

1. Stride-2 access on 32 lanes (`s[2*lane]`): conflict degree?
2. Why does broadcast (all lanes read one address) not conflict?
3. With `[32][33]`, which bank does `tile[4][7]` use?
4. Conflict degree of `s[8*lane]`?
5. Why does an odd stride never conflict?
6. Name one advantage of swizzling over padding.

<details class="answers">
<summary>Show answers</summary>

1. 2-way.
2. broadcast.
3. word 4·33 + 7 = 139 ⇒ bank 139 mod 32 = 11.
4. 8-way.
5. gcd(odd, 32) = 1.
6. keeps power-of-two pitch and vector alignment.

</details>

## Practice

[CU-030 Matrix Transpose](problem:CU-030)

*PMPP reference:* Ch. 5 (shared memory), Ch. 6 (bank conflicts are covered under shared-memory performance considerations), Ch. 11 (scan and bank-conflict avoidance).

## Further reading

- NVIDIA CUDA C++ Programming Guide and Best Practices Guide; NCCL documentation
