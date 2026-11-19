__global__ void relu(const float* X, float* Y, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) Y[i] = fmaxf(X[i], 0.0f);
}
