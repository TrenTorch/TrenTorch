__global__ void cos_partials(const float* A, const float* B, float* partial, int N) {
    extern __shared__ float s[];
    int t = threadIdx.x;
    int n = blockDim.x;
    float dot = 0.0f, aa = 0.0f, bb = 0.0f;
    for (int i = blockIdx.x * blockDim.x + t; i < N; i += blockDim.x * gridDim.x) {
        float a = A[i], b = B[i];
        dot = fmaf(a, b, dot);
        aa = fmaf(a, a, aa);
        bb = fmaf(b, b, bb);
    }
    s[t] = dot;
    s[n + t] = aa;
    s[2 * n + t] = bb;
    __syncthreads();
    for (int d = n / 2; d > 0; d >>= 1) {
        if (t < d) {
            s[t] += s[t + d];
            s[n + t] += s[n + t + d];
            s[2 * n + t] += s[2 * n + t + d];
        }
        __syncthreads();
    }
    if (t == 0) {
        partial[3 * blockIdx.x] = s[0];
        partial[3 * blockIdx.x + 1] = s[n];
        partial[3 * blockIdx.x + 2] = s[2 * n];
    }
}

__global__ void cos_final(const float* partial, float* out, int blocks) {
    extern __shared__ float s[];
    int t = threadIdx.x;
    int n = blockDim.x;
    s[t] = (t < blocks) ? partial[3 * t] : 0.0f;
    s[n + t] = (t < blocks) ? partial[3 * t + 1] : 0.0f;
    s[2 * n + t] = (t < blocks) ? partial[3 * t + 2] : 0.0f;
    __syncthreads();
    for (int d = n / 2; d > 0; d >>= 1) {
        if (t < d) {
            s[t] += s[t + d];
            s[n + t] += s[n + t + d];
            s[2 * n + t] += s[2 * n + t + d];
        }
        __syncthreads();
    }
    if (t == 0) out[0] = s[0] * rsqrtf(s[n]) * rsqrtf(s[2 * n]);
}
