__global__ void attention(const float* Q, const float* Kmat, const float* V, float* O, int T, int D) {
    __shared__ float q[64];
    __shared__ float scores[64];
    int row = blockIdx.x;
    int t = threadIdx.x;
    // TODO: 1) stage q  2) score[t] = dot(q, K[t]) / sqrt(D)  3) stable softmax over scores  4) O[row][t] = sum_j p[j] * V[j][t]
}
