#define TILE 16

__global__ void matmul_tiled(const float* A, const float* B, float* C, int M, int N, int K) {
    __shared__ float As[TILE][TILE];
    __shared__ float Bs[TILE][TILE];
    int row = blockIdx.y * TILE + threadIdx.y;
    int col = blockIdx.x * TILE + threadIdx.x;
    float acc = 0.0f;
    for (int tile = 0; tile < (K + TILE - 1) / TILE; ++tile) {
        int ak = tile * TILE + threadIdx.x;
        int bk = tile * TILE + threadIdx.y;
        As[threadIdx.y][threadIdx.x] = (row < M && ak < K) ? A[row * K + ak] : 0.0f;
        Bs[threadIdx.y][threadIdx.x] = (bk < K && col < N) ? B[bk * N + col] : 0.0f;
        __syncthreads();
        for (int k = 0; k < TILE; ++k) acc = fmaf(As[threadIdx.y][k], Bs[k][threadIdx.x], acc);
        __syncthreads();
    }
    if (row < M && col < N) C[row * N + col] = acc;
}
