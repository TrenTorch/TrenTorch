import java.util.ArrayDeque;
import java.util.Deque;
import java.util.ArrayList;
import java.util.Arrays;

public class Main {
    // O(n) time, O(k) space
    static long[] slidingWindowMax(long[] nums, long k) {
        int n = nums.length;
        int windowSize = (int) k;
        Deque<Integer> deque = new ArrayDeque<>();
        ArrayList<Long> result = new ArrayList<>(n - windowSize + 1);
        for (int i = 0; i < n; i++) {
            while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[i]) {
                deque.pollLast();
            }
            deque.addLast(i);
            if (deque.peekFirst() <= i - windowSize) {
                deque.pollFirst();
            }
            if (i >= windowSize - 1) {
                result.add(nums[deque.peekFirst()]);
            }
        }
        long[] out = new long[result.size()];
        for (int i = 0; i < result.size(); i++) {
            out[i] = result.get(i);
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(slidingWindowMax(new long[]{1L, 3L, -1L, -3L, 5L, 3L, 6L, 7L}, 3L)));
    }
}
