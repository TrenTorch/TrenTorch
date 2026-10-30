import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n * S) time, O(S) space where S is the sum of nums
    static long findTargetSumWays(long[] nums, long target) {
        Map<Long, Long> ways = new HashMap<>();
        ways.put(0L, 1L);
        for (long x : nums) {
            Map<Long, Long> next = new HashMap<>();
            for (Map.Entry<Long, Long> entry : ways.entrySet()) {
                long s = entry.getKey();
                long count = entry.getValue();
                next.merge(s + x, count, Long::sum);
                next.merge(s - x, count, Long::sum);
            }
            ways = next;
        }
        return ways.getOrDefault(target, 0L);
    }

    public static void main(String[] args) {
        System.out.println(findTargetSumWays(new long[]{1L, 1L, 1L, 1L, 1L}, 3L));
    }
}
