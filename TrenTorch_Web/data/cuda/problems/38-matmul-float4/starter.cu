__global__ void matmul_vec4(const float* A, const float* B, float* C, int M, int N, int K) {
    // TODO: one float4 of B per k, four accumulators, one float4 store into C.
}
