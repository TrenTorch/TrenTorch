import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) time, O(n) space
    static long countPairsWithSum(long[] nums, long target) {
        Map<Long, Long> seen = new HashMap<>();
        long count = 0;
        for (long x : nums) {
            count += seen.getOrDefault(target - x, 0L);
            seen.merge(x, 1L, Long::sum);
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countPairsWithSum(new long[]{1L, 2L, 3L, 4L, 3L}, 6L));
    }
}
