import java.util.HashMap;

public class Main {
    // O(n) time, O(n) space
    static long countSubarraysSumK(long[] nums, long k) {
        HashMap<Long, Long> seen = new HashMap<>();
        seen.put(0L, 1L);
        long prefix = 0;
        long count = 0;
        for (long x : nums) {
            prefix += x;
            count += seen.getOrDefault(prefix - k, 0L);
            seen.put(prefix, seen.getOrDefault(prefix, 0L) + 1);
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countSubarraysSumK(new long[]{1L, 1L, 1L}, 2L));
    }
}
