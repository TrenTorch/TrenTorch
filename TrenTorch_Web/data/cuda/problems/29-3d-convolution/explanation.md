### Direct baseline
```cpp
__global__ void conv3d_direct(const float* X, const float* F, float* Y,
                             int D, int H, int W,
                             int KD, int KH, int KW) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    int z = blockIdx.z * blockDim.z + threadIdx.z;
    if (x >= W || y >= H || z >= D) return;
    int rx = KW/2, ry = KH/2, rz = KD/2;
    float acc = 0.f;
    for (int kz=0; kz<KD; ++kz)
      for (int ky=0; ky<KH; ++ky)
        for (int kx=0; kx<KW; ++kx) {
          int ix=x+kx-rx, iy=y+ky-ry, iz=z+kz-rz;
          if (ix>=0 && ix<W && iy>=0 && iy<H && iz>=0 && iz<D)
            acc=fmaf(X[(iz*H+iy)*W+ix], F[(kz*KH+ky)*KW+kx], acc);
        }
    Y[(z*H+y)*W+x]=acc;
}
```

### Optimization strategy
A full 3D shared-memory tile includes halo in all three dimensions and can become large quickly. Consider:
- Tiling only the dimensions with useful reuse (2.5D tiling).
- Sliding a tile through depth while retaining a small number of planes.
- Using read-only/cache paths for filter/input data when appropriate.
- Choosing tile shape to keep x contiguous and preserve coalescing.
- Measuring shared-memory use, registers, and occupancy before increasing tile size.

### Optimality discussion
The direct kernel is a correctness baseline, not necessarily efficient for large filters. A shared tile lowers redundant global traffic but adds synchronization and resource pressure. The best design depends on volume dimensions, filter size, cache behavior, and GPU shared-memory capacity.

---
