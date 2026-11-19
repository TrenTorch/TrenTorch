__global__ void matmul_vec4(const float* A, const float* B, float* C, int M, int N, int K) {
    int c = blockIdx.x * blockDim.x + threadIdx.x;      // group of 4 columns
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    if (row < M && c < N / 4) {
        float4 acc;
        acc.x = 0.0f; acc.y = 0.0f; acc.z = 0.0f; acc.w = 0.0f;
        for (int k = 0; k < K; ++k) {
            float a = A[row * K + k];
            float4 b = reinterpret_cast<const float4*>(B + k * N)[c];
            acc.x += a * b.x;
            acc.y += a * b.y;
            acc.z += a * b.z;
            acc.w += a * b.w;
        }
        reinterpret_cast<float4*>(C + row * N)[c] = acc;
    }
}
