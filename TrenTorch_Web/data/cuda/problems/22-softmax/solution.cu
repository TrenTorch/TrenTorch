__global__ void softmax_rows(const float* X, float* Y, int rows, int K) {
    __shared__ float s[128];
    int row = blockIdx.x;
    int t = threadIdx.x;
    const float* x = X + row * K;
    float* y = Y + row * K;

    // 1) row maximum
    float m = -INFINITY;
    for (int j = t; j < K; j += blockDim.x) m = fmaxf(m, x[j]);
    s[t] = m;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] = fmaxf(s[t], s[t + d]);
        __syncthreads();
    }
    m = s[0];
    __syncthreads();

    // 2) sum of exponentials relative to the maximum
    float sum = 0.0f;
    for (int j = t; j < K; j += blockDim.x) sum += expf(x[j] - m);
    s[t] = sum;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    sum = s[0];

    // 3) normalise
    for (int j = t; j < K; j += blockDim.x) y[j] = expf(x[j] - m) / sum;
}
