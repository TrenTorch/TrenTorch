__global__ void double_it(const float* X, float* Y, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) Y[i] = X[i] * 2.0f;   // the grid is rounded up, so the last block has idle threads
}
