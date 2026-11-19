__global__ void bitonic_step(float* data, int j, int k, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    int l = i ^ j;
    if (l > i) {
        bool ascending = ((i & k) == 0);
        float a = data[i], b = data[l];
        if ((ascending && a > b) || (!ascending && a < b)) {
            data[i] = b;
            data[l] = a;
        }
    }
}
