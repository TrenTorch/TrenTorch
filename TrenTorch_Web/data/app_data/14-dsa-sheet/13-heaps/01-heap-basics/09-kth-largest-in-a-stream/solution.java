import java.util.PriorityQueue;
import java.util.ArrayList;
import java.util.Arrays;

public class Main {
    // O((n+m) log k) time, O(k) space
    static long[] kthLargestStream(long k, long[] nums, long[] adds) {
        int kInt = (int) k;
        PriorityQueue<Long> minHeap = new PriorityQueue<>();
        for (long x : nums) {
            minHeap.offer(x);
            if (minHeap.size() > kInt) {
                minHeap.poll();
            }
        }
        ArrayList<Long> result = new ArrayList<>();
        for (long x : adds) {
            minHeap.offer(x);
            if (minHeap.size() > kInt) {
                minHeap.poll();
            }
            result.add(minHeap.peek());
        }
        long[] ans = new long[result.size()];
        for (int i = 0; i < result.size(); i++) {
            ans[i] = result.get(i);
        }
        return ans;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(kthLargestStream(3L, new long[]{4L, 5L, 8L, 2L}, new long[]{3L, 5L, 10L, 9L, 4L})));
    }
}
