### Direct kernel
```cpp
__global__ void conv1d(const float* x, const float* w, float* y,
                       int N, int R) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float acc = 0.f;
        for (int k = -R; k <= R; ++k) {
            int j = i + k;
            if (j >= 0 && j < N) acc = fmaf(x[j], w[k + R], acc);
        }
        y[i] = acc;
    }
}
```

### Optimization
If the filter is small and shared by all blocks, constant memory may broadcast coefficients efficiently. A shared-memory input tile can load a contiguous region plus `R` halo elements on each side, reducing redundant global loads. Synchronize after tile loading and before reuse. Shared-memory tiling is useful only when reuse outweighs synchronization and occupancy costs.
