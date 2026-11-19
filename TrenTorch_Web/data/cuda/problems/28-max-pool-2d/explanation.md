### Kernel
```cpp
__global__ void maxpool2d(const float* X, float* Y,
                          int H, int W, int OH, int OW,
                          int PH, int PW, int SH, int SW) {
    int ox = blockIdx.x * blockDim.x + threadIdx.x;
    int oy = blockIdx.y * blockDim.y + threadIdx.y;
    if (ox < OW && oy < OH) {
        float m = -CUDART_INF_F;
        for (int ky = 0; ky < PH; ++ky)
          for (int kx = 0; kx < PW; ++kx) {
            int iy = oy * SH + ky, ix = ox * SW + kx;
            if (iy < H && ix < W)
              m = fmaxf(m, X[iy * W + ix]);
          }
        Y[oy * OW + ox] = m;
    }
}
```

### Analysis
The kernel is a small local reduction. Adjacent outputs often overlap input windows, so caches or shared-memory tiles can reuse values. For small windows, direct loads are frequently competitive. Check exact padding and NaN semantics against the reference operator.
