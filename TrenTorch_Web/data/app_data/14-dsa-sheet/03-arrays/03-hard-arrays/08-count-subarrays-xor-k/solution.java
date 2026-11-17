import java.util.HashMap;

public class Main {
    // O(n) time, O(n) space
    static long countSubarraysXorK(long[] nums, long k) {
        HashMap<Long, Long> seen = new HashMap<>();
        seen.put(0L, 1L);
        long prefix = 0;
        long count = 0;
        for (long x : nums) {
            prefix ^= x;
            count += seen.getOrDefault(prefix ^ k, 0L);
            seen.merge(prefix, 1L, Long::sum);
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countSubarraysXorK(new long[]{4L, 2L, 2L, 6L, 4L}, 6L));
    }
}
