__global__ void rms_norm(const float* X, const float* W, float* Y, int rows, int K, float eps) {
    __shared__ float s[128];
    // TODO: block-reduce sum of squares of this row, then scale.
}
