public class Main {
    // O(n log D) time, O(1) space
    static long minDaysBouquets(long[] bloom, long m, long k) {
        if (m * k > bloom.length) {
            return -1;
        }
        long lo = bloom[0];
        long hi = bloom[0];
        for (long b : bloom) {
            if (b < lo) lo = b;
            if (b > hi) hi = b;
        }
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (possible(bloom, mid, m, k)) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    private static boolean possible(long[] bloom, long day, long m, long k) {
        long bouquets = 0;
        long run = 0;
        for (long b : bloom) {
            if (b <= day) {
                run++;
                if (run == k) {
                    bouquets++;
                    run = 0;
                    if (bouquets >= m) return true;
                }
            } else {
                run = 0;
            }
        }
        return bouquets >= m;
    }

    public static void main(String[] args) {
        System.out.println(minDaysBouquets(new long[]{1L, 10L, 3L, 10L, 2L}, 3L, 1L));
    }
}
