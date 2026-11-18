import java.util.Arrays;
import java.util.Comparator;

public class Main {
    // O(n log n) time, O(n) space
    static long jobScheduling(long[][] jobs) {
        long[][] items = jobs.clone();
        Arrays.sort(items, Comparator.comparingLong((long[] j) -> j[1]));
        int n = items.length;
        long[] ends = new long[n];
        for (int i = 0; i < n; i++) {
            ends[i] = items[i][1];
        }
        long[] best = new long[n + 1];
        for (int i = 1; i <= n; i++) {
            long start = items[i - 1][0];
            long profit = items[i - 1][2];
            int before = bisectRight(ends, start, 0, i - 1);
            best[i] = Math.max(best[i - 1], profit + best[before]);
        }
        return best[n];
    }

    // index in [lo, hi) of the first value greater than x (same as Python bisect_right)
    static int bisectRight(long[] a, long x, int lo, int hi) {
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (x < a[mid]) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        System.out.println(jobScheduling(new long[][]{new long[]{1L, 3L, 50L}, new long[]{2L, 4L, 10L}, new long[]{3L, 5L, 40L}, new long[]{3L, 6L, 70L}}));
    }
}
