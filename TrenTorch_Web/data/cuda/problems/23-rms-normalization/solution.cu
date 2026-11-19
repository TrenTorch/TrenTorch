__global__ void rms_norm(const float* X, const float* W, float* Y, int rows, int K, float eps) {
    __shared__ float s[128];
    int row = blockIdx.x;
    int t = threadIdx.x;
    const float* x = X + row * K;
    float* y = Y + row * K;

    float acc = 0.0f;
    for (int j = t; j < K; j += blockDim.x) acc += x[j] * x[j];
    s[t] = acc;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    float inv_rms = rsqrtf(s[0] / K + eps);
    for (int j = t; j < K; j += blockDim.x) y[j] = x[j] * inv_rms * W[j];
}
