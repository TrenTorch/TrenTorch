### Direct correctness baseline
```cpp
__global__ void conv2d_direct(const float* X, const float* F, float* Y,
                             int H, int W, int FH, int FW) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x >= W || y >= H) return;
    int rx = FW / 2, ry = FH / 2;
    float acc = 0.f;
    for (int ky = 0; ky < FH; ++ky)
      for (int kx = 0; kx < FW; ++kx) {
        int ix = x + kx - rx, iy = y + ky - ry;
        if (ix >= 0 && ix < W && iy >= 0 && iy < H)
          acc = fmaf(X[iy * W + ix], F[ky * FW + kx], acc);
      }
    Y[y * W + x] = acc;
}
```

### Shared-memory design
A block producing `Tx x Ty` outputs loads an input tile of `(Tx+2Rx) x (Ty+2Ry)` values. Threads cooperatively load the tile, including halo cells; all threads reach `__syncthreads()`; valid output threads compute from the tile. This reduces repeated global loads between neighboring output pixels.

### Trade-offs
Larger tiles improve reuse but consume more shared memory and can reduce resident blocks. Filter coefficients may use constant memory when access is uniform. Compare against direct/global-cache kernels for small filters and small images.
