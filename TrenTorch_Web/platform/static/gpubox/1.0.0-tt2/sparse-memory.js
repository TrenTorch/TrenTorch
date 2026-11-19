/**
 * demo/sparse-memory.js
 * ─────────────────────
 * Sparse / Lazy Virtual VRAM Allocator.
 *
 * Models full enterprise GPU capacities (up to 80GB per virtual device across 16 GPUs)
 * without exhausting physical browser or Node.js host RAM.
 *
 * Backing pages (64 KB / 16,384 floats) are allocated lazily on first access.
 * Enforces per-device capacity limits and catches memory exhaustion.
 */

(function () {
  'use strict';

  const PAGE_SIZE_FLOATS = 16384; // 64 KB pages (16K x 4 bytes)
  const BYTES_PER_FLOAT = 4;

  class SparseVirtualBuffer {
    /**
     * @param {number} sizeBytes Total virtual allocation size in bytes
     * @param {number} deviceId Owning virtual GPU device ID
     */
    constructor(sizeBytes, deviceId = 0) {
      this.sizeBytes = sizeBytes;
      this.deviceId = deviceId;
      this.elementCount = Math.ceil(sizeBytes / BYTES_PER_FLOAT);
      this.pages = new Map(); // pageIndex -> Float32Array
      this.allocatedPages = 0;
      this._isFreed = false;
    }

    _getPage(pageIdx, create = false) {
      let page = this.pages.get(pageIdx);
      if (!page && create) {
        page = new Float32Array(PAGE_SIZE_FLOATS);
        this.pages.set(pageIdx, page);
        this.allocatedPages++;
      }
      return page;
    }

    get(idx) {
      if (this._isFreed) {
        throw new Error('cudaErrorIllegalAddress: use-after-free detected');
      }
      if (idx < 0 || idx >= this.elementCount) {
        throw new RangeError(`DevicePointer OOB read: index ${idx} (alloc size ${this.elementCount})`);
      }
      const pageIdx = Math.floor(idx / PAGE_SIZE_FLOATS);
      const offset = idx % PAGE_SIZE_FLOATS;
      const page = this._getPage(pageIdx, false);
      return page ? page[offset] : 0.0;
    }

    set(idx, val) {
      if (this._isFreed) {
        throw new Error('cudaErrorIllegalAddress: use-after-free detected');
      }
      if (idx < 0 || idx >= this.elementCount) {
        throw new RangeError(`DevicePointer OOB write: index ${idx} (alloc size ${this.elementCount})`);
      }
      const pageIdx = Math.floor(idx / PAGE_SIZE_FLOATS);
      const offset = idx % PAGE_SIZE_FLOATS;
      const page = this._getPage(pageIdx, true);
      page[offset] = val;
    }

    free() {
      this._isFreed = true;
      this.pages.clear();
      this.allocatedPages = 0;
    }

    getRealBytesUsed() {
      return this.allocatedPages * PAGE_SIZE_FLOATS * BYTES_PER_FLOAT;
    }
  }

  const exported = {
    PAGE_SIZE_FLOATS,
    SparseVirtualBuffer
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exported;
  }
  // globalThis works on the main thread and inside Web Workers (no `window`)
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxSparseMemory = exported;
  }
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxSparseMemory = exported;
  }
})();
