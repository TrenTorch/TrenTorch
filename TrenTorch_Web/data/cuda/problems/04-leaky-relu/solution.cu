__global__ void leaky_relu(const float* X, float* Y, int N, float alpha) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float x = X[i];
        Y[i] = (x >= 0.0f) ? x : alpha * x;
    }
}
