import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) time, O(n) space
    static long longestZeroSumSubarray(long[] nums) {
        Map<Long, Integer> first = new HashMap<>();
        first.put(0L, -1);
        long prefix = 0;
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            prefix += nums[i];
            Integer firstIndex = first.get(prefix);
            if (firstIndex != null) {
                best = Math.max(best, i - firstIndex);
            } else {
                first.put(prefix, i);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestZeroSumSubarray(new long[]{15L, -2L, 2L, -8L, 1L, 7L, 10L, 23L}));
    }
}
