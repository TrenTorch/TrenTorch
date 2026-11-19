### Typical failure
Rank 0 enqueues `AllReduce` then `Broadcast`, while rank 1 enqueues `Broadcast` then `AllReduce`. The ranks wait for different collectives and can hang.

### Debug checklist
- Verify every rank executes the same collective sequence.
- Match count, datatype, reduction op, root, and communicator.
- Ensure all ranks join communicator initialization and error handling.
- Check CUDA stream ordering and host-thread/device assignment.
- Log rank plus collective sequence number before each call.
- Use NCCL debug logging and a minimal two-rank reproducer.

### Fix
Make collective order identical on all ranks, including error/early-exit paths. A rank must not skip a collective that peers enter.
