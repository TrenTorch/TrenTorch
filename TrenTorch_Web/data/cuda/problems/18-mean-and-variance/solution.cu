__global__ void mean_var(const float* X, float* out, int N) {
    __shared__ float s[256];
    int t = threadIdx.x;

    // pass 1: mean
    float acc = 0.0f;
    for (int i = t; i < N; i += blockDim.x) acc += X[i];
    s[t] = acc;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    float mean = s[0] / N;
    __syncthreads();

    // pass 2: squared deviations from the mean
    acc = 0.0f;
    for (int i = t; i < N; i += blockDim.x) {
        float dx = X[i] - mean;
        acc += dx * dx;
    }
    s[t] = acc;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) s[t] += s[t + d];
        __syncthreads();
    }
    if (t == 0) {
        out[0] = mean;
        out[1] = s[0] / N;
    }
}
