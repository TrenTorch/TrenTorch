public class Main {
    // O(n log M) time, O(1) space where M = max(piles)
    static long minEatingSpeed(long[] piles, long hours) {
        long lo = 1;
        long hi = 0;
        for (long p : piles) {
            if (p > hi) hi = p;
        }
        while (lo < hi) {
            long mid = (lo + hi) >>> 1;
            long needed = 0;
            for (long p : piles) {
                needed += (p + mid - 1) / mid;
            }
            if (needed <= hours) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        System.out.println(minEatingSpeed(new long[]{3L, 6L, 7L, 11L}, 8L));
    }
}
