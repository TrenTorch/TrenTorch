# Threads, blocks, grids and indexing

## Three nested levels

A launch creates a **grid** of **blocks**, each block holding **threads**. You choose the shape:
```cuda
kernel<<<gridDim, blockDim>>>(...);
```
Inside the kernel, built-in variables tell a thread who it is: `threadIdx` (position in its block), `blockIdx` (position of its block in the grid), `blockDim` (threads per block), `gridDim` (blocks in the grid). Each has `.x`, `.y`, `.z`.

<div class="cuda-diagram" data-diagram="grid-of-blocks" data-title="A grid of blocks of threads"></div>

## The global index

For a 1D layout:

$$\text{idx} = \text{blockIdx.x} \times \text{blockDim.x} + \text{threadIdx.x}$$

Think of blocks as pages of a notebook with `blockDim.x` lines each: `blockIdx.x` is the page, `threadIdx.x` the line, `idx` the line number counted from the start of the notebook.

## Sizing the grid

To cover `N` elements with blocks of `B` threads you need $\lceil N/B \rceil$ blocks, written in integers as `(N + B - 1) / B`.

## Bounds check

Rounding up creates extra threads past the end of the data. Guard them:
```cuda
int i = blockIdx.x * blockDim.x + threadIdx.x;
if (i < n) { /* ... work on element i ... */ }
```
Without the guard those threads read and write memory they do not own.

**Worked example.** `N = 6`, block size 4. Grid = ⌈6/4⌉ = 2 blocks, 8 threads. Block 0 computes idx 0-3; block 1 computes idx 4, 5, 6, 7. Threads 6 and 7 fail `i < 6` and do nothing.

## 2D layouts for matrices

Row-major matrix of width `W`: element (row, col) sits at `row * W + col`. Map `x` to columns and `y` to rows:
```cuda
int col = blockIdx.x * blockDim.x + threadIdx.x;
int row = blockIdx.y * blockDim.y + threadIdx.y;
```
Putting `x` on the column axis matters for memory speed (chapter D1): consecutive `threadIdx.x` values then touch consecutive addresses.

## Limits

At most 1,024 threads per block (product of x, y, z). `gridDim.x` can be huge (up to 2³¹−1); `y` and `z` are limited to 65,535.

## Linearized thread id

Inside a block the hardware numbers threads in one line: `tid = threadIdx.x + threadIdx.y * blockDim.x + threadIdx.z * blockDim.x * blockDim.y`. This number, not the 2D coordinates, decides which warp a thread belongs to (chapter B3).

## Interactive: Who am I?

<div class="cuda-viz" data-viz="VIZ-INDEX-CALCULATOR" data-title="Who am I?" data-spec="VIZ-INDEX-CALCULATOR"></div>

## Interactive: Covering a matrix

<div class="cuda-viz" data-viz="VIZ-GRID-BUILDER" data-title="Covering a matrix" data-spec="VIZ-GRID-BUILDER"></div>

## Generalizing to 3D

Linearized thread id inside a block and the global 3D → 1D index for a volume of `X × Y × Z` stored x-fastest:
$$\text{tid} = t_x + t_y B_x + t_z B_x B_y,\qquad \text{voxel} = (z \cdot Y + y)\cdot X + x$$
with each coordinate computed as `blockIdx.c * blockDim.c + threadIdx.c`. The same "x is the contiguous axis" rule applies (D1).

## Grid size limits and the 2D grid trick

`gridDim.x` ≤ 2³¹ − 1; `gridDim.y`, `gridDim.z` ≤ 65,535. For a huge 1D problem, either use a grid-stride loop (E1) or fold the block index: `blk = blockIdx.x + blockIdx.y * gridDim.x`.

## Integer overflow: when `int` is not enough

`blockIdx.x * blockDim.x` is computed in 32-bit `unsigned`/`int` arithmetic. With N = 3 × 10⁹ floats (12 GB, fits on an 80 GB card) the product wraps around and every thread past 2³¹ reads the wrong element.
```cuda
size_t i = (size_t)blockIdx.x * blockDim.x + threadIdx.x;   // widen BEFORE multiplying
```
Also compute byte offsets in `size_t`. This is a classic "works until the dataset grows" bug.

## Choosing the 2D block shape by warp analysis

For a W-wide row-major matrix and a block `(Bx, By)`: a warp covers `32/Bx` rows when Bx < 32. Each row-segment is `Bx × 4` bytes contiguous. Efficiency of a *row-major* read:
- Bx = 32: one 128 B segment per warp → 4 sectors, 100%.
- Bx = 16: two 64 B segments → 4 sectors, still 100% if each segment is sector-aligned.
- Bx = 8: four 32 B segments → 4 sectors, 100% *if* aligned; but small segments make misalignment cost more (a 32 B segment straddling a sector boundary touches 2 sectors).
Rule: prefer **Bx ≥ 32** (or a multiple of 8 floats) for coalescing; tile heights fill the rest of the block.

## Check yourself

1. N = 1,000,000 and blockDim = 256. How many blocks?
2. Which element does thread 3 of block 5 handle when blockDim = 128?
3. Why can a kernel with no bounds check appear to work on some sizes and crash on others?
4. N = 3 × 10⁹. Which variable types must be 64-bit in the index calculation?
5. A 33×33 volume of cells is processed with 8×8×4 blocks. How many blocks in each dimension?

<details class="answers">
<summary>Show answers</summary>

1. 3,907 blocks.
2. 5·128 + 3 = 643.
3. Out-of-bounds writes may land in padded or unrelated allocations.
4. the index and any byte offset: `size_t`.
5. ⌈33/8⌉ = 5, 5, ⌈33/4⌉ = 9.

</details>

## Pitfalls

- Forgetting the bounds check.
- Integer division: `N / B` rounds down; use `(N + B - 1) / B`.
- Swapping row/col axes.

## Practice

[CU-001 Vector Addition](problem:CU-001) · [CU-002 Hadamard Product](problem:CU-002) · [CU-009 Matrix Addition](problem:CU-009) · [CU-010 Outer Product](problem:CU-010)

*PMPP reference:* Ch. 2 (index calculation, grid sizing), Ch. 3 (multidimensional grids, linearizing 2D/3D arrays, image blur and matrix examples).
