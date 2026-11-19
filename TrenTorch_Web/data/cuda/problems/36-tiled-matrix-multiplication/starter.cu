#define TILE 16

__global__ void matmul_tiled(const float* A, const float* B, float* C, int M, int N, int K) {
    __shared__ float As[TILE][TILE];
    __shared__ float Bs[TILE][TILE];
    // TODO: loop over K tiles: load, __syncthreads(), multiply-accumulate, __syncthreads().
}
