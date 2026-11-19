__global__ void softmax_rows(const float* X, float* Y, int rows, int K) {
    __shared__ float s[128];
    int row = blockIdx.x;
    // TODO: 1) block-reduce the row max  2) block-reduce sum of exp(x - max)  3) write exp(x - max) / sum
}
