### Kernel
```cpp
__global__ void relu(const float* X, float* Y, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) Y[i] = fmaxf(X[i], 0.0f);
}
```

### Analysis and trade-offs
This is one read and one write per element: `8N` bytes, with a tiny amount of arithmetic. `fmaxf` expresses a max operation without explicit control-flow branching. NaN behavior can differ among `fmaxf`, comparison/select expressions, and framework semantics; verify the required contract.

**Optimization:** Fuse ReLU into a preceding matrix multiply or following epilogue to avoid a full intermediate write/read round trip.
