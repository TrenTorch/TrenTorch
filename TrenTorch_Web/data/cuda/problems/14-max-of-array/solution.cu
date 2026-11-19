__global__ void max_partials(const float* X, float* partial, int N) {
    extern __shared__ float s[];
    unsigned t = threadIdx.x;
    unsigned i = blockIdx.x * blockDim.x + t;
    s[t] = (i < N) ? X[i] : -CUDART_INF_F;
    __syncthreads();
    for (unsigned d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] = fmaxf(s[t], s[t + d]);
        __syncthreads();
    }
    if (t == 0) partial[blockIdx.x] = s[0];
}

__global__ void max_final(const float* partial, float* out, int blocks) {
    extern __shared__ float s[];
    unsigned t = threadIdx.x;
    s[t] = (t < blocks) ? partial[t] : -CUDART_INF_F;
    __syncthreads();
    for (unsigned d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] = fmaxf(s[t], s[t + d]);
        __syncthreads();
    }
    if (t == 0) out[0] = s[0];
}
