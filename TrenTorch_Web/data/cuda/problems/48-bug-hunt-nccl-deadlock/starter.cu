#include <cuda_runtime.h>
#include <nccl.h>
#include <cstdio>

int main() {
    const int n = 2;
    const int count = 4;
    ncclComm_t comms[2];
    ncclCommInitAll(comms, n);

    float *d_a[2];
    float *d_b[2];
    float h_val[4];
    for (int r = 0; r < n; r++) {
        for (int i = 0; i < count; i++) h_val[i] = r + 1;
        cudaSetDevice(r);
        cudaMalloc(&d_a[r], count * sizeof(float));
        cudaMalloc(&d_b[r], count * sizeof(float));
        cudaMemcpy(d_a[r], h_val, count * sizeof(float), cudaMemcpyHostToDevice);
    }

    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        if (r == 0) {
            ncclAllReduce(d_a[r], d_b[r], count, ncclFloat, ncclSum, comms[r], 0);
            ncclBroadcast(d_b[r], d_b[r], count, ncclFloat, 0, comms[r], 0);
        } else {
            ncclBroadcast(d_b[r], d_b[r], count, ncclFloat, 0, comms[r], 0);
            ncclAllReduce(d_a[r], d_b[r], count, ncclFloat, ncclSum, comms[r], 0);
        }
    }

    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        cudaMemcpy(h_val, d_b[r], count * sizeof(float), cudaMemcpyDeviceToHost);
        printf("rank %d: %f\n", r, h_val[0]);
    }
    return 0;
}
