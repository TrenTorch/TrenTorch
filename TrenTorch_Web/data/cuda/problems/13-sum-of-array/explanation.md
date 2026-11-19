### Two-stage design
```cpp
__global__ void sum_partials(const float* X, float* partial, int N) {
    extern __shared__ float s[];
    unsigned t = threadIdx.x;
    unsigned i = blockIdx.x * blockDim.x + t;
    float v = (i < N) ? X[i] : 0.0f;
    s[t] = v;
    __syncthreads();

    for (unsigned d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    if (t == 0) partial[blockIdx.x] = s[0];
}

__global__ void sum_final(const float* partial, float* out, int blocks) {
    extern __shared__ float s[];
    unsigned t = threadIdx.x;
    float v = (t < blocks) ? partial[t] : 0.0f;
    s[t] = v;
    __syncthreads();
    for (unsigned d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    if (t == 0) *out = s[0];
}
```
The final kernel's block size must be at least `blocks` or it must itself use a loop over partials. Production code should use warp shuffles or a tested block-reduction primitive to reduce synchronization overhead.

### Analysis
Each input is read once; partial sums are written and reread. The extra traffic is small relative to a large input, while two launches avoid unsafe global synchronization. A single `atomicAdd` per block is a simpler alternative, but floating-point accumulation order is nondeterministic and contention may matter.
