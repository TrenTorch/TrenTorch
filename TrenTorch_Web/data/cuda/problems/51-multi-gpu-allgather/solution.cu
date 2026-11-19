#include <cuda_runtime.h>
#include <nccl.h>
#include <cstdio>

int main() {
    const int n = 4;          // GPUs
    const int shard = 4;      // floats per shard
    ncclComm_t comms[4];
    ncclCommInitAll(comms, n);

    float *d_send[4];
    float *d_recv[4];
    float h_val[4];
    for (int r = 0; r < n; r++) {
        for (int i = 0; i < shard; i++) h_val[i] = r + 1;
        cudaSetDevice(r);
        cudaMalloc(&d_send[r], shard * sizeof(float));
        cudaMalloc(&d_recv[r], n * shard * sizeof(float));
        cudaMemcpy(d_send[r], h_val, shard * sizeof(float), cudaMemcpyHostToDevice);
    }

    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        ncclAllGather(d_send[r], d_recv[r], shard, ncclFloat, comms[r], 0);
    }

    float h_out[16];
    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        cudaMemcpy(h_out, d_recv[r], n * shard * sizeof(float), cudaMemcpyDeviceToHost);
        printf("rank %d: %f %f %f %f\n", r, h_out[0], h_out[4], h_out[8], h_out[12]);
    }
    return 0;
}
