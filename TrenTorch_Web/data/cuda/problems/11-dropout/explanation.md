### Simple deterministic hash-based example
```cpp
__device__ __forceinline__ unsigned hash32(unsigned x) {
    x ^= x >> 16; x *= 0x7feb352du;
    x ^= x >> 15; x *= 0x846ca68bu;
    x ^= x >> 16;
    return x;
}

__global__ void dropout_hash(const float* X, float* Y, int N,
                             float keep_prob, unsigned seed) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        unsigned r = hash32((unsigned)i ^ seed);
        float u = (r >> 8) * (1.0f / 16777216.0f);
        Y[i] = (u < keep_prob) ? X[i] / keep_prob : 0.0f;
    }
}
```

### Critical caveat
This hash illustrates deterministic index-based mask generation; it is not a substitute for a statistically validated production RNG contract. A production implementation should use a well-defined counter-based or cuRAND generator, define stream/offset semantics, and ensure independent masks across calls as required. Handle `keep_prob == 0` explicitly and define inference behavior.
