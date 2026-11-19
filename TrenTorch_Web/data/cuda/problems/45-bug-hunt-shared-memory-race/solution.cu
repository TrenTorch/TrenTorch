__global__ void block_reverse(const float* in, float* out, int n) {
    __shared__ float s[128];
    int t = threadIdx.x;
    int i = blockIdx.x * blockDim.x + t;
    s[t] = in[i];
    __syncthreads();   // every producer must finish before any thread reads another thread's element
    out[i] = s[blockDim.x - 1 - t];
}
