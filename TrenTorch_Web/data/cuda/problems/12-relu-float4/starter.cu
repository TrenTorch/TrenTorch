__global__ void relu_float4(const float* X, float* Y, int N) {
    int v = blockIdx.x * blockDim.x + threadIdx.x;
    int vec_count = N / 4;
    // TODO: process float4 number v if it exists, then one tail element per thread.
}
