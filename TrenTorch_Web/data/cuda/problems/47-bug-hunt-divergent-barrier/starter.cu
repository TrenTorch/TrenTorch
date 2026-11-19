__global__ void reverse_valid(const float* in, float* out, int valid) {
    __shared__ float s[64];
    int t = threadIdx.x;
    if (t < valid) {
        s[t] = in[t];
        __syncthreads();
    }
    out[t] = (63 - t < valid) ? s[63 - t] : 0.0f;
}
