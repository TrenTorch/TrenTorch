__global__ void dot_partials(const float* A, const float* B, float* partial, int N) {
    extern __shared__ float s[];
    unsigned t = threadIdx.x;
    unsigned stride = blockDim.x * gridDim.x;
    float acc = 0.0f;
    for (unsigned i = blockIdx.x * blockDim.x + t; i < N; i += stride) acc = fmaf(A[i], B[i], acc);
    s[t] = acc;
    __syncthreads();
    for (unsigned d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    if (t == 0) partial[blockIdx.x] = s[0];
}

__global__ void dot_final(const float* partial, float* out, int blocks) {
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
