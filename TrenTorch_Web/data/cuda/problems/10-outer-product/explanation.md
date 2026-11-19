### Kernel
```cpp
__global__ void outer_product(const float* a, const float* b,
                              float* C, int M, int N) {
    int j = blockIdx.x * blockDim.x + threadIdx.x;
    int i = blockIdx.y * blockDim.y + threadIdx.y;
    if (i < M && j < N) C[(size_t)i * N + j] = a[i] * b[j];
}
```

### Analysis
The output dominates traffic (`4MN` bytes). Threads in a row read the same `a[i]` and adjacent `b[j]` values; caches and broadcast behavior can reuse `a[i]`. For large outputs, output bandwidth is a major lower bound. A tiled design can explicitly reuse vector values, but may not beat the simple kernel for all shapes.
