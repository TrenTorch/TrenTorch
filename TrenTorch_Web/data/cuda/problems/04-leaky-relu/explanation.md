### Kernel
```cpp
__global__ void leaky_relu(const float* X, float* Y,
                           int N, float alpha) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float x = X[i];
        Y[i] = (x >= 0.0f) ? x : alpha * x;
    }
}
```

### Analysis
The branch condition is data-dependent, but the compiler may lower the select to predicated instructions. A branch is not automatically harmful: neighboring lanes with similar signs may have little divergence, and the compiler chooses instruction forms based on target architecture. The operation is generally bandwidth-bound.

**Validation:** Test positive, negative, zero, infinities, and NaNs against the required reference semantics.
