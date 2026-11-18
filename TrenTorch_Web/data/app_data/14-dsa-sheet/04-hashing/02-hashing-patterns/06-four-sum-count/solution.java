import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n^2) time, O(n^2) space
    static long fourSumCount(long[] a, long[] b, long[] c, long[] d) {
        Map<Long, Long> sums = new HashMap<>();
        for (long x : a) {
            for (long y : b) {
                long s = x + y;
                sums.put(s, sums.getOrDefault(s, 0L) + 1);
            }
        }
        long ans = 0;
        for (long z : c) {
            for (long w : d) {
                long target = -(z + w);
                ans += sums.getOrDefault(target, 0L);
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        System.out.println(fourSumCount(new long[]{1L, 2L}, new long[]{-2L, -1L}, new long[]{-1L, 2L}, new long[]{0L, 2L}));
    }
}
