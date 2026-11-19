__global__ void fused_scale_mask_softmax(const float* X, const int* mask, float* Y, int rows, int K, float scale) {
    __shared__ float s[128];
    int row = blockIdx.x;
    int t = threadIdx.x;
    const float* x = X + row * K;
    const int* mk = mask + row * K;
    float* y = Y + row * K;

    float m = -INFINITY;
    for (int j = t; j < K; j += blockDim.x) {
        if (mk[j] != 0) m = fmaxf(m, scale * x[j]);
    }
    s[t] = m;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] = fmaxf(s[t], s[t + d]);
        __syncthreads();
    }
    m = s[0];
    __syncthreads();

    float sum = 0.0f;
    for (int j = t; j < K; j += blockDim.x) {
        if (mk[j] != 0) sum += expf(scale * x[j] - m);
    }
    s[t] = sum;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    sum = s[0];

    for (int j = t; j < K; j += blockDim.x) {
        y[j] = (mk[j] != 0 && sum > 0.0f) ? expf(scale * x[j] - m) / sum : 0.0f;
    }
}
