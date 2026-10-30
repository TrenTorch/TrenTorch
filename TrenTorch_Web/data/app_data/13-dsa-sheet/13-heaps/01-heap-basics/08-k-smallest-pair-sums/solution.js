// O(k log min(n1, k)) time, O(min(n1, k)) space
function kSmallestPairSums(nums1, nums2, k) {
    if (!nums1.length || !nums2.length || k <= 0) {
        return [];
    }

    const heap = [];

    function push(item) {
        heap.push(item);
        let idx = heap.length - 1;
        while (idx > 0) {
            const parentIdx = Math.floor((idx - 1) / 2);
            if (heap[parentIdx][0] <= heap[idx][0]) break;
            [heap[parentIdx], heap[idx]] = [heap[idx], heap[parentIdx]];
            idx = parentIdx;
        }
    }

    function pop() {
        if (heap.length === 0) return undefined;
        const top = heap[0];
        const end = heap.pop();
        if (heap.length > 0) {
            heap[0] = end;
            let idx = 0;
            const length = heap.length;
            while (true) {
                let leftIdx = 2 * idx + 1;
                let rightIdx = 2 * idx + 2;
                let smallest = idx;
                if (leftIdx < length && heap[leftIdx][0] < heap[smallest][0]) {
                    smallest = leftIdx;
                }
                if (rightIdx < length && heap[rightIdx][0] < heap[smallest][0]) {
                    smallest = rightIdx;
                }
                if (smallest === idx) break;
                [heap[idx], heap[smallest]] = [heap[smallest], heap[idx]];
                idx = smallest;
            }
        }
        return top;
    }

    const n1 = nums1.length;
    const n2 = nums2.length;
    const limit = Math.min(n1, k);

    for (let i = 0; i < limit; i++) {
        push([nums1[i] + nums2[0], i, 0]);
    }

    const out = [];
    while (heap.length > 0 && out.length < k) {
        const [total, i, j] = pop();
        out.push(total);
        if (j + 1 < n2) {
            push([nums1[i] + nums2[j + 1], i, j + 1]);
        }
    }

    return out;
}

console.log(kSmallestPairSums([1, 7, 11], [2, 4, 6], 3));
