__global__ void matmul_naive(const float* A, const float* B, float* C, int M, int N, int K) {
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    if (row < M && col < N) {
        float acc = 0.0f;
        for (int k = 0; k < K; ++k) acc = fmaf(A[row * K + k], B[k * N + col], acc);
        C[row * N + col] = acc;
    }
}
