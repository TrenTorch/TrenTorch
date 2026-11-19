### Kernel
```cpp
__global__ void gelu_exact(const float* X, float* Y, int N) {
    constexpr float inv_sqrt2 = 0.7071067811865475f;
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float x = X[i];
        Y[i] = 0.5f * x * (1.0f + erff(x * inv_sqrt2));
    }
}
```

### Analysis
The kernel has one input read and one output write, but `erff` is much more expensive than a simple add or multiply. Consequently, the arithmetic/instruction cost per byte is higher than ReLU or vector addition. Approximate tanh GELU is a different function and should not silently replace exact GELU.
