__global__ void warp_sum_kernel(const float* X, float* out, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    float v = (i < N) ? X[i] : 0.0f;
    for (int offset = 16; offset > 0; offset >>= 1) {
        v += __shfl_down_sync(0xffffffff, v, offset);
    }
    if (threadIdx.x == 0) out[blockIdx.x] = v;
}
