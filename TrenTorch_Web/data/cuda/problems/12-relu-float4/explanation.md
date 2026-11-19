### Scalar baseline
Use CU-003 as the correctness reference.

### Vectorized kernel
```cpp
__global__ void relu_float4(const float* X, float* Y, int N) {
    int vec_count = N / 4;
    int v = blockIdx.x * blockDim.x + threadIdx.x;
    if (v < vec_count) {
        const float4 x = reinterpret_cast<const float4*>(X)[v];
        float4 y;
        y.x = fmaxf(x.x, 0.0f);
        y.y = fmaxf(x.y, 0.0f);
        y.z = fmaxf(x.z, 0.0f);
        y.w = fmaxf(x.w, 0.0f);
        reinterpret_cast<float4*>(Y)[v] = y;
    }
    // A separate scalar tail kernel or a guarded tail in this kernel is required.
}
```
A complete single-launch variant can let a small set of threads handle the tail:
```cpp
__global__ void relu_float4_tail(const float* X, float* Y, int N) {
    int v = blockIdx.x * blockDim.x + threadIdx.x;
    int vec_count = N / 4;
    if (v < vec_count) {
        float4 x = reinterpret_cast<const float4*>(X)[v], y;
        y.x=fmaxf(x.x,0.f); y.y=fmaxf(x.y,0.f);
        y.z=fmaxf(x.z,0.f); y.w=fmaxf(x.w,0.f);
        reinterpret_cast<float4*>(Y)[v]=y;
    }
    int i = vec_count * 4 + v;
    if (i < N) Y[i] = fmaxf(X[i], 0.0f);
}
```

### Alignment and performance
`float4` requires suitable alignment (normally 16-byte aligned addresses). If pointers are not guaranteed aligned, use a scalar prologue or fallback. The tail logic above is safe because only the final at-most-three elements are processed by the `i` path; launch enough threads to cover both the vector count and tail indices. Vectorization reduces instruction/address-generation overhead and can improve memory instruction efficiency, but it does not reduce the minimum `8N` bytes transferred. Benchmark against the compiler's scalarized code.

---
