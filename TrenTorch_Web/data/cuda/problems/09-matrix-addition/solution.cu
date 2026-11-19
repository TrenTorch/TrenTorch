__global__ void matrix_add(const float* A, const float* B, float* C, int H, int W) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x < W && y < H) {
        int i = y * W + x;
        C[i] = A[i] + B[i];
    }
}
