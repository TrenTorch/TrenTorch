/**
 * demo/desync-detector.js
 * ───────────────────────
 * Multi-GPU Collective Desync & Deadlock Detector.
 *
 * Catches the most notorious multi-GPU distributed failures without hanging:
 *   - Missing ranks: rank never reaches collective (e.g. rank 7 missing while others wait)
 *   - Parameter mismatch: ranks passing different count, datatype, op, or root
 *   - Order mismatch: ranks calling collectives in different order (e.g. AllReduce then Broadcast vs Broadcast then AllReduce)
 *   - Unmatched Send/Recv in point-to-point transfers
 */

(function () {
  'use strict';

  class NcclDesyncError extends Error {
    constructor(details) {
      super(details.message);
      this.name = 'NcclDesyncError';
      this.category = 'NcclDesyncError';
      this.details = details;
    }
  }

  class CollectiveDesyncDetector {
    constructor() {
      this.pendingPosts = new Map(); // commId -> Map<seq, Map<rank, post>>
      this.rankSeq = new Map();      // `${commId}:${rank}` -> current seq
      this.history = [];
      this.ptpPosts = new Map();     // commId -> { sends: [], recvs: [] }
    }

    getNextSeq(commId, rank) {
      const key = `${commId}:${rank}`;
      const seq = this.rankSeq.get(key) || 0;
      this.rankSeq.set(key, seq + 1);
      return seq;
    }

    /**
     * Post a collective operation for a rank.
     * @param {Object} post
     * @param {number} post.commId Communicator ID
     * @param {number} post.nranks Total ranks in communicator
     * @param {number} post.rank Calling rank
     * @param {string} post.op Operation ('allreduce', 'broadcast', 'allgather', 'reducescatter', 'reduce')
     * @param {number} post.count Element count
     * @param {string} post.datatype Data type ('float32', etc.)
     * @param {number} [post.root] Root rank (for broadcast/reduce)
     * @param {string} [post.reduceOp] Reduction op ('sum', 'max', etc.)
     * @param {number} [post.callSite] Source line number if available
     * @returns {Object} Collective verification status
     */
    postCollective(post) {
      const commId = post.commId || 0;
      const rank = post.rank;
      const seq = this.getNextSeq(commId, rank);
      post.seq = seq;

      if (!this.pendingPosts.has(commId)) {
        this.pendingPosts.set(commId, new Map());
      }
      const commMap = this.pendingPosts.get(commId);

      if (!commMap.has(seq)) {
        commMap.set(seq, new Map());
      }
      const seqMap = commMap.get(seq);
      seqMap.set(rank, post);

      // Check if all expected ranks in this communicator have reached this collective sequence
      if (seqMap.size === post.nranks) {
        // All ranks have arrived for this sequence. Validate cross-rank alignment!
        this.validateCollectiveAlignment(seq, seqMap, post.nranks);
        // Complete collective
        commMap.delete(seq);
        this.history.push({ seq, commId, op: post.op, ranks: post.nranks, status: 'MATCHED' });
        return { completed: true, seq };
      }

      return { completed: false, seq, arrivedCount: seqMap.size };
    }

    validateCollectiveAlignment(seq, seqMap, nranks) {
      const ranks = Array.from(seqMap.keys());
      const first = seqMap.get(ranks[0]);

      for (let i = 1; i < ranks.length; i++) {
        const other = seqMap.get(ranks[i]);

        // 1. Order / Op mismatch
        if (other.op !== first.op) {
          throw new NcclDesyncError({
            type: 'ORDER_MISMATCH',
            seq,
            message: `Collective order mismatch at sequence #${seq}: rank ${first.rank} posted "${first.op}" while rank ${other.rank} posted "${other.op}"`,
            rankA: first.rank,
            opA: first.op,
            rankB: other.rank,
            opB: other.op,
            callSite: other.callSite
          });
        }

        // 2. Count mismatch
        if (other.count !== first.count) {
          throw new NcclDesyncError({
            type: 'COUNT_MISMATCH',
            seq,
            message: `Collective parameter mismatch at sequence #${seq}: rank ${other.rank} posted count=${other.count} while rank ${first.rank} posted count=${first.count}`,
            offendingRank: other.rank,
            parameter: 'count',
            expected: first.count,
            actual: other.count,
            callSite: other.callSite
          });
        }

        // 3. Datatype mismatch
        if (other.datatype !== first.datatype) {
          throw new NcclDesyncError({
            type: 'DATATYPE_MISMATCH',
            seq,
            message: `Collective parameter mismatch at sequence #${seq}: rank ${other.rank} posted datatype="${other.datatype}" while rank ${first.rank} posted datatype="${first.datatype}"`,
            offendingRank: other.rank,
            parameter: 'datatype',
            expected: first.datatype,
            actual: other.datatype,
            callSite: other.callSite
          });
        }

        // 4. Root mismatch
        if (first.root !== undefined && other.root !== first.root) {
          throw new NcclDesyncError({
            type: 'ROOT_MISMATCH',
            seq,
            message: `Collective parameter mismatch at sequence #${seq}: rank ${other.rank} posted root=${other.root} while rank ${first.rank} posted root=${first.root}`,
            offendingRank: other.rank,
            parameter: 'root',
            expected: first.root,
            actual: other.root,
            callSite: other.callSite
          });
        }

        // 5. Reduction op mismatch
        if (first.reduceOp !== undefined && other.reduceOp !== first.reduceOp) {
          throw new NcclDesyncError({
            type: 'REDUCE_OP_MISMATCH',
            seq,
            message: `Collective parameter mismatch at sequence #${seq}: rank ${other.rank} posted reduction op="${other.reduceOp}" while rank ${first.rank} posted op="${first.reduceOp}"`,
            offendingRank: other.rank,
            parameter: 'reduceOp',
            expected: first.reduceOp,
            actual: other.reduceOp,
            callSite: other.callSite
          });
        }
      }
    }

    /**
     * Check for unreached ranks / deadlocks across pending collective posts.
     * @param {number} commId
     * @param {number} nranks
     */
    checkDeadlocks(commId, nranks) {
      if (!this.pendingPosts.has(commId)) return;
      const commMap = this.pendingPosts.get(commId);

      for (const [seq, seqMap] of commMap.entries()) {
        if (seqMap.size > 0 && seqMap.size < nranks) {
          const waitingRanks = Array.from(seqMap.keys()).sort((a, b) => a - b);
          const missingRanks = [];
          for (let r = 0; r < nranks; r++) {
            if (!seqMap.has(r)) missingRanks.push(r);
          }

          throw new NcclDesyncError({
            type: 'COLLECTIVE_DEADLOCK',
            seq,
            message: `Collective deadlock at sequence #${seq}: rank ${missingRanks.join(',')} missing, ranks ${waitingRanks.join(',')} waiting`,
            missingRanks,
            waitingRanks
          });
        }
      }
    }

    // Point-to-Point group tracking
    postSend(commId, srcRank, dstRank, count, datatype) {
      if (!this.ptpPosts.has(commId)) {
        this.ptpPosts.set(commId, { sends: [], recvs: [] });
      }
      this.ptpPosts.get(commId).sends.push({ srcRank, dstRank, count, datatype });
    }

    postRecv(commId, dstRank, srcRank, count, datatype) {
      if (!this.ptpPosts.has(commId)) {
        this.ptpPosts.set(commId, { sends: [], recvs: [] });
      }
      this.ptpPosts.get(commId).recvs.push({ srcRank, dstRank, count, datatype });
    }

    validateGroupPtp(commId) {
      const group = this.ptpPosts.get(commId);
      if (!group) return;

      const { sends, recvs } = group;

      for (const s of sends) {
        const matchIdx = recvs.findIndex(r => r.srcRank === s.srcRank && r.dstRank === s.dstRank && r.count === s.count);
        if (matchIdx === -1) {
          throw new NcclDesyncError({
            type: 'UNMATCHED_SEND',
            message: `Unmatched point-to-point transfer: rank ${s.srcRank} posted ncclSend to peer ${s.dstRank}, but rank ${s.dstRank} did not post matching ncclRecv`,
            srcRank: s.srcRank,
            dstRank: s.dstRank
          });
        }
      }

      for (const r of recvs) {
        const matchIdx = sends.findIndex(s => s.srcRank === r.srcRank && s.dstRank === r.dstRank && s.count === r.count);
        if (matchIdx === -1) {
          throw new NcclDesyncError({
            type: 'UNMATCHED_RECV',
            message: `Unmatched point-to-point transfer: rank ${r.dstRank} posted ncclRecv from peer ${r.srcRank}, but rank ${r.srcRank} did not post matching ncclSend`,
            srcRank: r.srcRank,
            dstRank: r.dstRank
          });
        }
      }

      this.ptpPosts.delete(commId);
    }

    reset() {
      this.pendingPosts.clear();
      this.rankSeq.clear();
      this.history = [];
      this.ptpPosts.clear();
    }
  }

  const exported = {
    NcclDesyncError,
    CollectiveDesyncDetector
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exported;
  }
  // globalThis works on the main thread and inside Web Workers (no `window`)
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxDesyncDetector = exported;
  }
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxDesyncDetector = exported;
  }
})();
