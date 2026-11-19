__global__ void mean_var(const float* X, float* out, int N) {
    __shared__ float s[256];
    // TODO: pass 1: block-reduce the sum to get the mean. Pass 2: block-reduce (x - mean)^2.
}
