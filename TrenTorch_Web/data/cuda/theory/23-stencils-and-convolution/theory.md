# Stencils and convolution

## Neighbourhood operations

In a **stencil** or **convolution** each output depends on a neighbourhood of inputs. A 1D filter of width K reads K inputs per output; a 3×3 2D filter reads 9; a 3D 3×3×3 filter reads 27. Neighbouring outputs share most of their inputs, so there is real reuse to exploit.

## Boundary handling

Near the edges the neighbourhood falls outside the array. Decide the rule (zero padding, clamp, or "valid" convolution that only produces interior outputs) and guard every read.

## Tiling with a halo

A block that computes a `T`-wide output tile needs `T + K − 1` inputs: the tile plus a **halo** of `(K−1)/2` cells on each side. Load that region into shared memory once, synchronize, then every thread reads its K neighbours from shared memory.

Loads per output: without tiling = K; with tiling ≈ (T + K − 1) / T. For a 2D 3×3 filter with a 16×16 output tile the block loads 18 × 18 = 324 inputs for 256 outputs: 1.27 per output instead of 9, about **7× fewer** global loads.

## Constant memory for the filter

Every thread reads the same filter weights in the same order: a perfect fit for constant memory (D6), which broadcasts them.

## Pooling

Max pooling reduces each window to one value. When the stride equals the window size, windows do not overlap, so there is **no reuse** and tiling adds nothing: just make sure the reads are coalesced.

## Higher dimensions

3D convolution has the same structure; shared-memory tiles grow cubically, so tile sizes are small and the halo overhead is a larger fraction.

## Interactive: Tile plus a halo

<div class="cuda-viz" data-viz="VIZ-HALO-TILE" data-title="Tile plus a halo" data-spec="VIZ-HALO-TILE"></div>

## FLOP and byte counting for direct convolution

For a conv layer with batch N, input channels C_in, output channels C_out, output size H × W, kernel K × K:
$$\text{FLOPs} = 2\cdot N\cdot C_{out}\cdot H\cdot W\cdot C_{in}\cdot K^2$$
Example: N = 32, C_in = 64, C_out = 128, H = W = 56, K = 3 → 2 · 32 · 128 · 3,136 · 64 · 9 = **14.8 GFLOP**. Input = 32·64·56·56·4 B = 25.7 MB; output = 32·128·3,136·4 B = 51.4 MB; weights = 128·64·9·4 = 295 KB. Ideal bytes ≈ 77 MB → AI ≈ **192 FLOP/B**: strongly compute-bound *if* data reuse is perfect, which is why convolutions are implemented as GEMM or with large register tiles.

## Convolution as GEMM (im2col)

Build a matrix of shape (N·H·W) × (C_in·K²) = 100,352 × 576 (4 B each = **231 MB**, i.e. 9× the input) and multiply by a (C_in·K²) × C_out filter matrix. The GEMM then reaches high AI but the im2col buffer costs memory traffic. **Implicit GEMM** forms the tiles on the fly inside the kernel from the original tensor, avoiding the 231 MB buffer (the basis of cuDNN-style kernels). Winograd and FFT trade multiplications for additions/transforms for small/large K respectively *(context only)*.

## Separable filters

A K × K filter that factors as an outer product `a bᵀ` can be applied as two 1D passes: MACs per output **2K instead of K²** (3×3: 6 vs 9; 7×7: 14 vs 49). Gaussian blur and many classical filters are separable; learned conv filters generally are not.

## Halo overhead formula

2D tile T_x × T_y with an (K−1)/2 halo: loads per output = (T_x+K−1)(T_y+K−1)/(T_x·T_y). 16×16 with K = 3: 324/256 = 1.27; K = 5: 400/256 = 1.56; K = 7: 484/256 = 1.89. 3D tile 8×8×8 with K = 3: 10³/8³ = **1.95**; K = 5: 12³/512 = 3.4 (why 3D tiles suffer).

## Interactive: Convolution as a big matrix

<div class="cuda-viz" data-viz="VIZ-IM2COL" data-title="Convolution as a big matrix" data-spec="VIZ-IM2COL"></div>

## Check yourself

1. 1D filter K = 5, output tile T = 128. How many input elements does a block load?
2. Why is constant memory a good home for filter weights?
3. Does tiling help a stride-2, 2×2 max pool? Why not?
4. FLOPs of a 1×1 convolution with C_in = C_out = 256 on a 14 × 14 map, batch 1?
5. Halo overhead (loads per output) for K = 5, tile 16 × 16?
6. Why can't a stride-2 2×2 max-pool use shared-memory tiling profitably?

<details class="answers">
<summary>Show answers</summary>

1. 132.
2. uniform broadcast reads.
3. windows don't overlap: no reuse.
4. 2·196·256·256 = 25.7 MFLOP.
5. 1.56.
6. no overlap.

</details>

## Practice

[CU-026 1D Convolution](problem:CU-026) · [CU-027 2D Convolution](problem:CU-027) · [CU-028 Max Pool 2D](problem:CU-028) · [CU-029 3D Convolution](problem:CU-029)

*PMPP reference:* Ch. 7 (convolution: constant memory for filters, tiled convolution with halo cells, caching of halo cells in L2), Ch. 8 (stencil: 3D tiling, thread coarsening, register tiling), Ch. 16 (convolutional layers as matrix multiplication: im2col).
