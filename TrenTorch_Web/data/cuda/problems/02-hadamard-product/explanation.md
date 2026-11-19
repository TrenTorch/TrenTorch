### Kernel
```cpp
__global__ void hadamard(const float* A, const float* B,
                         float* C, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) C[i] = A[i] * B[i];
}
```

### Analysis
The traffic is `12N` bytes: read `A`, read `B`, write `C`. There is one multiply per element, giving very low arithmetic intensity. For large arrays, performance is bounded primarily by sustainable memory bandwidth:
`time >= 12N / effective_bandwidth`.
This is a lower-bound estimate, not a measured runtime.

### Optimization
Coalesce all three streams; avoid unnecessary temporary tensors; fuse with producers/consumers. Vectorized loads are only worthwhile if alignment, tail handling, and compiler-generated code are verified.

**Complexity:** `O(N)` work and traffic.
