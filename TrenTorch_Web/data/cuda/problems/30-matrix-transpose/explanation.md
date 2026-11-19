### Naive baseline
```cpp
__global__ void transpose_naive(const float* A, float* B, int H, int W) {
    int x=blockIdx.x*blockDim.x+threadIdx.x;
    int y=blockIdx.y*blockDim.y+threadIdx.y;
    if (x<W && y<H) B[(size_t)x*H+y]=A[(size_t)y*W+x];
}
```
Reads are coalesced, but writes are strided across lanes (or vice versa depending on mapping).

### Tiled implementation
```cpp
__global__ void transpose_tiled(const float* A, float* B, int H, int W) {
    __shared__ float tile[32][33];
    int x = blockIdx.x * 32 + threadIdx.x;
    int y = blockIdx.y * 32 + threadIdx.y;
    if (x < W && y < H) tile[threadIdx.y][threadIdx.x] = A[(size_t)y*W+x];
    __syncthreads();
    int ox = blockIdx.y * 32 + threadIdx.x;
    int oy = blockIdx.x * 32 + threadIdx.y;
    if (ox < H && oy < W) B[(size_t)oy*H+ox] = tile[threadIdx.x][threadIdx.y];
}
```

### Why `[32][33]`
Padding the second dimension avoids the classic shared-memory bank-conflict pattern when threads read a transposed column. The tile makes both global reads and writes coalesced. Edge tiles require bounds checks. Ensure the chosen block shape and index mapping match the tile; common implementations use a 32-wide warp arrangement.
