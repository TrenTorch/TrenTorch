__global__ void matmul_coarsened(const float* A, const float* B, float* C, int M, int N, int K) {
    int row0 = blockIdx.y * 16 + threadIdx.y * 2;
    int col0 = blockIdx.x * 16 + threadIdx.x * 2;
    float acc00 = 0.0f, acc01 = 0.0f, acc10 = 0.0f, acc11 = 0.0f;
    for (int k = 0; k < K; ++k) {
        float a0 = (row0 < M) ? A[row0 * K + k] : 0.0f;
        float a1 = (row0 + 1 < M) ? A[(row0 + 1) * K + k] : 0.0f;
        float b0 = (col0 < N) ? B[k * N + col0] : 0.0f;
        float b1 = (col0 + 1 < N) ? B[k * N + col0 + 1] : 0.0f;
        acc00 += a0 * b0;
        acc01 += a0 * b1;
        acc10 += a1 * b0;
        acc11 += a1 * b1;
    }
    if (row0 < M && col0 < N) C[row0 * N + col0] = acc00;
    if (row0 < M && col0 + 1 < N) C[row0 * N + col0 + 1] = acc01;
    if (row0 + 1 < M && col0 < N) C[(row0 + 1) * N + col0] = acc10;
    if (row0 + 1 < M && col0 + 1 < N) C[(row0 + 1) * N + col0 + 1] = acc11;
}
