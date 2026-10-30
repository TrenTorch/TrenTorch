import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(n) time, O(n) space
    static long longestWithinLimit(long[] nums, long limit) {
        Deque<Integer> maxDeque = new ArrayDeque<>();
        Deque<Integer> minDeque = new ArrayDeque<>();
        int left = 0;
        long best = 0;
        for (int right = 0; right < nums.length; right++) {
            long x = nums[right];
            while (!maxDeque.isEmpty() && nums[maxDeque.peekLast()] <= x) {
                maxDeque.pollLast();
            }
            maxDeque.offerLast(right);
            while (!minDeque.isEmpty() && nums[minDeque.peekLast()] >= x) {
                minDeque.pollLast();
            }
            minDeque.offerLast(right);
            while (nums[maxDeque.peekFirst()] - nums[minDeque.peekFirst()] > limit) {
                left++;
                if (maxDeque.peekFirst() < left) {
                    maxDeque.pollFirst();
                }
                if (minDeque.peekFirst() < left) {
                    minDeque.pollFirst();
                }
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestWithinLimit(new long[]{8L, 2L, 4L, 7L}, 4L));
    }
}
