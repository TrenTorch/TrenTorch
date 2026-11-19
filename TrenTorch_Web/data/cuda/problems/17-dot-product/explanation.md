### Per-block kernel pattern
```cpp
__global__ void dot_partials(const float* A, const float* B,
                             float* partial, int N) {
    extern __shared__ float s[];
    unsigned t = threadIdx.x;
    size_t i = (size_t)blockIdx.x * blockDim.x + t;
    size_t stride = (size_t)blockDim.x * gridDim.x;
    float acc = 0.0f;
    for (; i < (size_t)N; i += stride) acc = fmaf(A[i], B[i], acc);
    s[t] = acc;
    __syncthreads();
    for (unsigned d = blockDim.x / 2; d; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    if (t == 0) partial[blockIdx.x] = s[0];
}
```
Reduce the partial array in a second kernel.

### Analysis
The input traffic is approximately `8N` bytes plus partial traffic; arithmetic is two operations per element (multiply-add, often fused). Use enough blocks to expose parallelism without creating an excessively large partial array. Numerical results depend on reduction order and FMA use.
