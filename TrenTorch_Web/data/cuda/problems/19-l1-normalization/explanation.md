### Recommended multi-stage approach
1. Reduce `sum(abs(x[i]))` to a scalar.
2. Launch a map kernel that divides each element by the scalar.
```cpp
__global__ void l1_map(const float* x, float* y, int n,
                       const float* denom) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = x[i] / *denom;
}
```
The reduction can use CU-013's pattern with `fabsf`.

### Caveats
Define behavior when the denominator is zero. A single ordinary kernel cannot safely let all blocks consume a globally complete sum without a supported grid-wide synchronization mechanism. Cooperative launch/grid synchronization has residency and launch constraints; do not replace it with an unsafe spin barrier.
