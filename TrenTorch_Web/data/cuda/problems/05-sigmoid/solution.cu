__global__ void sigmoid(const float* X, float* Y, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float x = X[i];
        Y[i] = 1.0f / (1.0f + expf(-x));
    }
}
