/**
 * demo/race-detector.js
 * ─────────────────────
 * Shared Memory & Multi-Thread Race Condition Detector.
 *
 * Implements barrier-epoch tracking across warps and threads within a CUDA thread block.
 * Detects:
 *   - Read-After-Write (RAW) hazard without intervening __syncthreads()
 *   - Write-After-Read (WAR) hazard without intervening __syncthreads()
 *   - Write-After-Write (WAW) hazard without intervening __syncthreads()
 *
 * Cross-warp hazard -> ERROR (throws RaceConditionError)
 * Same-warp hazard  -> WARNING (logged in diagnostic reports)
 */

(function () {
  'use strict';

  class RaceConditionError extends Error {
    constructor(details) {
      const msg = `Shared memory race hazard (${details.hazardType}) detected in kernel "${details.kernel}" ` +
        `at block (${details.block.x},${details.block.y},${details.block.z}) on array "${details.arrayName}[${details.index}]": ` +
        `Thread (${details.threadB.x},${details.threadB.y},${details.threadB.z}, warp ${details.warpB}) ${details.actionB} ` +
        `while Thread (${details.threadA.x},${details.threadA.y},${details.threadA.z}, warp ${details.warpA}) previously ${details.actionA} ` +
        `in the same barrier epoch ${details.epoch} without intervening __syncthreads()`;
      super(msg);
      this.name = 'RaceConditionError';
      this.category = 'RaceConditionError';
      this.details = details;
    }
  }

  class SharedMemoryRaceDetector {
    constructor(options = {}) {
      this.enabled = options.enabled !== false;
      this.strictRaces = options.strictRaces === true; // If true, same-warp also throws
      this.barrierEpoch = 0;
      this.records = new Map(); // key: `${arrayName}:${index}` -> { lastWrite, lastReads: [] }
      this.warnings = [];
      this.errors = [];
      this.kernelName = options.kernelName || 'unknownKernel';
      this.blockIdx = options.blockIdx || { x: 0, y: 0, z: 0 };
    }

    advanceBarrier() {
      this.barrierEpoch++;
      // Clear active access records for the new epoch
      this.records.clear();
    }

    recordAccess(arrayName, index, isWrite, ctx) {
      if (!this.enabled) return;

      const key = `${arrayName}:${index}`;
      let record = this.records.get(key);
      if (!record) {
        record = { lastWrite: null, lastReads: [] };
        this.records.set(key, record);
      }

      const linearIdx = (ctx && ctx.linearIdx !== undefined) ? ctx.linearIdx : ((ctx && ctx.threadIdx && ctx.threadIdx.x) || 0);
      const warpId = (ctx && ctx.warpId !== undefined) ? ctx.warpId : Math.floor(linearIdx / 32);
      const threadIdx = (ctx && ctx.threadIdx) ? { x: ctx.threadIdx.x || 0, y: ctx.threadIdx.y || 0, z: ctx.threadIdx.z || 0 } : { x: 0, y: 0, z: 0 };

      if (isWrite) {
        // Check for WAW race
        if (record.lastWrite && record.lastWrite.linearIdx !== linearIdx) {
          const isCrossWarp = record.lastWrite.warpId !== warpId;
          const details = {
            hazardType: isCrossWarp ? 'CROSS_WARP_WAW' : 'SAME_WARP_WAW',
            kernel: this.kernelName,
            block: this.blockIdx,
            arrayName,
            index,
            epoch: this.barrierEpoch,
            actionA: 'wrote',
            actionB: 'wrote',
            threadA: record.lastWrite.threadIdx,
            warpA: record.lastWrite.warpId,
            threadB: threadIdx,
            warpB: warpId
          };
          if (isCrossWarp || this.strictRaces) {
            const err = new RaceConditionError(details);
            this.errors.push(err);
            throw err;
          } else {
            this.warnings.push(details);
          }
        }

        // Check for WAR race
        for (const r of record.lastReads) {
          if (r.linearIdx !== linearIdx) {
            const isCrossWarp = r.warpId !== warpId;
            const details = {
              hazardType: isCrossWarp ? 'CROSS_WARP_WAR' : 'SAME_WARP_WAR',
              kernel: this.kernelName,
              block: this.blockIdx,
              arrayName,
              index,
              epoch: this.barrierEpoch,
              actionA: 'read',
              actionB: 'wrote',
              threadA: r.threadIdx,
              warpA: r.warpId,
              threadB: threadIdx,
              warpB: warpId
            };
            if (isCrossWarp || this.strictRaces) {
              const err = new RaceConditionError(details);
              this.errors.push(err);
              throw err;
            } else {
              this.warnings.push(details);
            }
          }
        }

        record.lastWrite = { linearIdx, warpId, threadIdx, epoch: this.barrierEpoch };
      } else {
        // Read access: check for RAW race
        if (record.lastWrite && record.lastWrite.linearIdx !== linearIdx) {
          const isCrossWarp = record.lastWrite.warpId !== warpId;
          const details = {
            hazardType: isCrossWarp ? 'CROSS_WARP_RAW' : 'SAME_WARP_RAW',
            kernel: this.kernelName,
            block: this.blockIdx,
            arrayName,
            index,
            epoch: this.barrierEpoch,
            actionA: 'wrote',
            actionB: 'read',
            threadA: record.lastWrite.threadIdx,
            warpA: record.lastWrite.warpId,
            threadB: threadIdx,
            warpB: warpId
          };
          if (isCrossWarp || this.strictRaces) {
            const err = new RaceConditionError(details);
            this.errors.push(err);
            throw err;
          } else {
            this.warnings.push(details);
          }
        }

        record.lastReads.push({ linearIdx, warpId, threadIdx, epoch: this.barrierEpoch });
      }
    }
  }

  const exported = {
    RaceConditionError,
    SharedMemoryRaceDetector
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exported;
  }
  // globalThis works on the main thread and inside Web Workers (no `window`)
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxRaceDetector = exported;
  }
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxRaceDetector = exported;
  }
})();
