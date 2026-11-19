__global__ void abs_sum_partials(const float* x, float* partial, int n) {
    extern __shared__ float s[];
    unsigned t = threadIdx.x;
    unsigned i = blockIdx.x * blockDim.x + t;
    s[t] = (i < n) ? fabsf(x[i]) : 0.0f;
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
    s[t] = (t < blocks) ? partial[t] : 0.0f;
    __syncthreads();
    for (unsigned d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    if (t == 0) out[0] = s[0];
}

__global__ void l1_map(const float* x, float* y, int n, const float* denom) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = x[i] / denom[0];
}
