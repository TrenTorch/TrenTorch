import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) expected time (hash map of prefix sums), O(n) space
    static long longestSubarraySumKAny(long[] nums, long k) {
        Map<Long, Integer> first = new HashMap<>();
        first.put(0L, -1);
        long prefix = 0;
        long best = 0;
        for (int i = 0; i < nums.length; i++) {
            prefix += nums[i];
            Integer start = first.get(prefix - k);
            if (start != null) {
                best = Math.max(best, i - start);
            }
            first.putIfAbsent(prefix, i);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestSubarraySumKAny(new long[]{1L, -1L, 5L, -2L, 3L}, 3L));
    }
}
