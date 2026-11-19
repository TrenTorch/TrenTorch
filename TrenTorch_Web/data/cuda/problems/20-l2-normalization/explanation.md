### Approach
Reduce sum of squares, then map:
```cpp
__global__ void l2_map(const float* x, float* y, int n,
                       const float* sumsq) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = x[i] * rsqrtf(*sumsq);
}
```
Use a two-stage reduction for `sumsq`. `rsqrtf` computes an approximate reciprocal square root; use `1.0f/sqrtf(v)` if the accuracy contract requires it. Define zero-norm behavior.
