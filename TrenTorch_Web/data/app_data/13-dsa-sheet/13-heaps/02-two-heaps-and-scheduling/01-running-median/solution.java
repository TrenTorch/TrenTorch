import java.util.PriorityQueue;
import java.util.Collections;
import java.util.Arrays;

public class Main {
    // O(n log n) time, O(n) space
    static double[] runningMedian(long[] nums) {
        if (nums == null || nums.length == 0) {
            return new double[0];
        }
        PriorityQueue<Long> low = new PriorityQueue<>(Collections.reverseOrder());
        PriorityQueue<Long> high = new PriorityQueue<>();
        double[] out = new double[nums.length];
        for (int i = 0; i < nums.length; i++) {
            long x = nums[i];
            low.add(x);
            high.add(low.poll());
            if (high.size() > low.size()) {
                low.add(high.poll());
            }
            if (low.size() > high.size()) {
                out[i] = (double) low.peek();
            } else {
                out[i] = (low.peek() + high.peek()) / 2.0;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runningMedian(new long[]{5L, 15L, 1L, 3L})));
    }
}
