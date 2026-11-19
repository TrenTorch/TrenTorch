__global__ void reverse_valid(const float* in, float* out, int valid) {
    __shared__ float s[64];
    int t = threadIdx.x;
    s[t] = (t < valid) ? in[t] : 0.0f;   // neutral value for inactive lanes
    __syncthreads();                      // reached by all 64 threads
    out[t] = s[63 - t];
}
