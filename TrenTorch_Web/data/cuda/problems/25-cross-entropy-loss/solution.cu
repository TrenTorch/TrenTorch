__global__ void cross_entropy(const float* Z, const int* target, float* loss, int rows, int K) {
    __shared__ float s[128];
    int row = blockIdx.x;
    int t = threadIdx.x;
    const float* z = Z + row * K;

    float m = -INFINITY;
    for (int j = t; j < K; j += blockDim.x) m = fmaxf(m, z[j]);
    s[t] = m;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] = fmaxf(s[t], s[t + d]);
        __syncthreads();
    }
    m = s[0];
    __syncthreads();

    float sum = 0.0f;
    for (int j = t; j < K; j += blockDim.x) sum += expf(z[j] - m);
    s[t] = sum;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    if (t == 0) loss[row] = m + logf(s[0]) - z[target[row]];
}
