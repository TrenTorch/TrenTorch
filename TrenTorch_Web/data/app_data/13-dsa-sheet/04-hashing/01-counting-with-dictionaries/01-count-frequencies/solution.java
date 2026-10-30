import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n + q) time, O(n) space
    static long[] countFrequencies(long[] nums, long[] queries) {
        Map<Long, Long> counts = new HashMap<>();
        for (long x : nums) {
            counts.merge(x, 1L, Long::sum);
        }
        long[] result = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            result[i] = counts.getOrDefault(queries[i], 0L);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(countFrequencies(new long[]{1L, 2L, 2L, 3L, 3L, 3L}, new long[]{3L, 2L, 5L})));
    }
}
