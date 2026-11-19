__global__ void transpose(const float* A, float* B, int H, int W) {
    __shared__ float tile[32][33];   // the extra column removes the bank conflicts

    int x = blockIdx.x * 32 + threadIdx.x;
    int y = blockIdx.y * 32 + threadIdx.y;
    if (x < W && y < H) tile[threadIdx.y][threadIdx.x] = A[y * W + x];
    __syncthreads();

    // Swap the block coordinates, keep threadIdx.x as the fast axis for the write.
    int ox = blockIdx.y * 32 + threadIdx.x;
    int oy = blockIdx.x * 32 + threadIdx.y;
    if (ox < H && oy < W) B[oy * H + ox] = tile[threadIdx.x][threadIdx.y];
}
