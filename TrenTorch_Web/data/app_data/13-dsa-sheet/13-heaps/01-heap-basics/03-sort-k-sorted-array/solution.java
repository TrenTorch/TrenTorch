import java.util.PriorityQueue;
import java.util.Arrays;

public class Main {
    // O(n log k) time, O(k) space
    static long[] sortKSorted(long[] nums, long k) {
        int n = nums.length;
        if (n == 0) return new long[0];
        int kInt = (int) k;
        int initialSize = Math.min(kInt + 1, n);
        PriorityQueue<Long> heap = new PriorityQueue<>();
        for (int i = 0; i < initialSize; i++) {
            heap.add(nums[i]);
        }
        long[] out = new long[n];
        int outIdx = 0;
        for (int i = initialSize; i < n; i++) {
            heap.add(nums[i]);
            out[outIdx++] = heap.poll();
        }
        while (!heap.isEmpty()) {
            out[outIdx++] = heap.poll();
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(sortKSorted(new long[]{6L, 5L, 3L, 2L, 8L, 10L, 9L}, 3L)));
    }
}
