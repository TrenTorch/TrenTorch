__global__ void scan_blocks(const float* x, float* y, float* sums, int n) {
    extern __shared__ float s[];
    int t = threadIdx.x;
    int i = blockIdx.x * blockDim.x + t;
    s[t] = (i < n) ? x[i] : 0.0f;
    __syncthreads();
    // Hillis-Steele: log2(256) steps, O(n log n) work, simple and branch-light.
    for (int off = 1; off < blockDim.x; off <<= 1) {
        float v = (t >= off) ? s[t - off] : 0.0f;
        __syncthreads();
        s[t] += v;
        __syncthreads();
    }
    if (i < n) y[i] = s[t];
    if (t == blockDim.x - 1) sums[blockIdx.x] = s[t];
}

__global__ void scan_sums(float* sums, int nb) {
    __shared__ float s[32];
    int t = threadIdx.x;
    s[t] = (t < nb) ? sums[t] : 0.0f;
    __syncthreads();
    for (int off = 1; off < blockDim.x; off <<= 1) {
        float v = (t >= off) ? s[t - off] : 0.0f;
        __syncthreads();
        s[t] += v;
        __syncthreads();
    }
    if (t < nb) sums[t] = s[t];
}

__global__ void add_offsets(float* y, const float* sums, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (blockIdx.x > 0 && i < n) y[i] += sums[blockIdx.x - 1];
}
