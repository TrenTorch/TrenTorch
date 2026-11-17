import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) time, O(n) space
    static long[] frequencyExtremes(long[] nums) {
        Map<Long, Long> counts = new HashMap<>();
        for (long x : nums) {
            counts.merge(x, 1L, Long::sum);
        }
        long most = 0, least = 0, mostCount = 0, leastCount = 0;
        boolean first = true;
        for (Map.Entry<Long, Long> e : counts.entrySet()) {
            long v = e.getKey();
            long c = e.getValue();
            if (first) {
                most = least = v;
                mostCount = leastCount = c;
                first = false;
                continue;
            }
            if (c > mostCount || (c == mostCount && v < most)) {
                most = v;
                mostCount = c;
            }
            if (c < leastCount || (c == leastCount && v < least)) {
                least = v;
                leastCount = c;
            }
        }
        return new long[]{most, least};
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(frequencyExtremes(new long[]{4L, 4L, 5L, 5L, 6L})));
    }
}
