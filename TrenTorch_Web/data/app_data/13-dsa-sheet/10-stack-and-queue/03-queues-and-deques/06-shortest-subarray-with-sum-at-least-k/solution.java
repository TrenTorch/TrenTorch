import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(n) time, O(n) space
    static long shortestSubarraySumK(long[] nums, long k) {
        int n = nums.length;
        long[] prefix = new long[n + 1];
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
        int best = n + 1;
        Deque<Integer> window = new ArrayDeque<>();
        for (int b = 0; b <= n; b++) {
            long p = prefix[b];
            while (!window.isEmpty() && p - prefix[window.peekFirst()] >= k) {
                best = Math.min(best, b - window.pollFirst());
            }
            while (!window.isEmpty() && prefix[window.peekLast()] >= p) {
                window.pollLast();
            }
            window.addLast(b);
        }
        return best <= n ? best : -1;
    }

    public static void main(String[] args) {
        System.out.println(shortestSubarraySumK(new long[]{2L, -1L, 2L}, 3L));
    }
}
