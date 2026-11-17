// O(n log k) time, O(k) space where k = ladders
class MinHeap {
    constructor() {
        this.heap = [];
    }
    push(val) {
        this.heap.push(val);
        this._bubbleUp(this.heap.length - 1);
    }
    pop() {
        if (this.heap.length === 0) return null;
        const min = this.heap[0];
        const end = this.heap.pop();
        if (this.heap.length > 0) {
            this.heap[0] = end;
            this._bubbleDown(0);
        }
        return min;
    }
    size() {
        return this.heap.length;
    }
    _bubbleUp(idx) {
        while (idx > 0) {
            const parentIdx = Math.floor((idx - 1) / 2);
            if (this.heap[parentIdx] <= this.heap[idx]) break;
            [this.heap[parentIdx], this.heap[idx]] = [this.heap[idx], this.heap[parentIdx]];
            idx = parentIdx;
        }
    }
    _bubbleDown(idx) {
        const length = this.heap.length;
        while (true) {
            let smallest = idx;
            const left = 2 * idx + 1;
            const right = 2 * idx + 2;
            if (left < length && this.heap[left] < this.heap[smallest]) {
                smallest = left;
            }
            if (right < length && this.heap[right] < this.heap[smallest]) {
                smallest = right;
            }
            if (smallest === idx) break;
            [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
            idx = smallest;
        }
    }
}

function furthestBuilding(heights, bricks, ladders) {
    const heap = new MinHeap();
    for (let i = 1; i < heights.length; i++) {
        const climb = heights[i] - heights[i - 1];
        if (climb <= 0) continue;
        heap.push(climb);
        if (heap.size() > ladders) {
            bricks -= heap.pop();
            if (bricks < 0) {
                return i - 1;
            }
        }
    }
    return heights.length - 1;
}

console.log(furthestBuilding([4, 2, 7, 6, 9, 14, 12], 5, 1));
