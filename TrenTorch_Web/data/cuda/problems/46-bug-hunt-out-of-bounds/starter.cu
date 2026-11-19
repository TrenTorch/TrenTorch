__global__ void double_it(const float* X, float* Y, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    Y[i] = X[i] * 2.0f;
}
