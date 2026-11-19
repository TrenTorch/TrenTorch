__global__ void cross_entropy(const float* Z, const int* target, float* loss, int rows, int K) {
    __shared__ float s[128];
    // TODO: row max, sum of exp(z - max), then loss = max + log(sum) - z[target].
}
