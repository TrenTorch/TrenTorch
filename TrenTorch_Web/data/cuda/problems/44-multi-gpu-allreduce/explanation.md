### Recommended implementation
Use NCCL:
```cpp
ncclAllReduce(sendbuf, recvbuf, count, ncclFloat,
              ncclSum, comm, stream);
```
Initialize one communicator per participating GPU/rank, select the correct device on each host thread, and enqueue collectives in the same order on all ranks.

### Ring intuition
A ring all-reduce performs reduce-scatter followed by all-gather. Each rank sends/receives chunks around the ring; bandwidth utilization can be high for large messages. Latency and topology matter for small messages and multi-node systems.

### Deadlock and correctness
All ranks must participate in matching collective calls with compatible counts, datatypes, operations, and order. Check NCCL return codes, communicator initialization, stream dependencies, and device/rank mapping. Do not hand-roll a ring unless required for the exercise; NCCL handles topology and protocol details.
