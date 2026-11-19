__global__ void gelu_exact(const float* X, float* Y, int N) {
    const float inv_sqrt2 = 0.7071067811865475f;
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float x = X[i];
        Y[i] = 0.5f * x * (1.0f + erff(x * inv_sqrt2));
    }
}
