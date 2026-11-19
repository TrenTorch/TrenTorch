__global__ void sumsq_partials(const float* x, float* partial, int n) {
    extern __shared__ float s[];
    unsigned t = threadIdx.x;
    unsigned i = blockIdx.x * blockDim.x + t;
    float v = (i < n) ? x[i] : 0.0f;
    s[t] = v * v;
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

__global__ void l2_map(const float* x, float* y, int n, const float* sumsq) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = x[i] * rsqrtf(sumsq[0]);
}
