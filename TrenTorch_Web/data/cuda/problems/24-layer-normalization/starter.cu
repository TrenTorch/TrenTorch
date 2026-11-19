__global__ void layer_norm(const float* X, const float* gamma, const float* beta, float* Y, int rows, int K, float eps) {
    __shared__ float s[128];
    // TODO: mean, then variance, then normalise with the affine parameters.
}
