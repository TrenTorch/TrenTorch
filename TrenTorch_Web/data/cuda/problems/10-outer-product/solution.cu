__global__ void outer_product(const float* a, const float* b, float* C, int M, int N) {
    int j = blockIdx.x * blockDim.x + threadIdx.x;
    int i = blockIdx.y * blockDim.y + threadIdx.y;
    if (i < M && j < N) C[i * N + j] = a[i] * b[j];
}
