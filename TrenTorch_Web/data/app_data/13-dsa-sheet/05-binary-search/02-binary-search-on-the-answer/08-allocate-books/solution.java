public class Main {
    // O(n log S) time, O(1) space, where n = pages.length, S = sum(pages)
    static long allocateBooks(long[] pages, long students) {
        if (students > pages.length) {
            return -1;
        }
        long lo = 0;
        long hi = 0;
        for (long p : pages) {
            if (p > lo) lo = p;
            hi += p;
        }
        while (lo < hi) {
            long mid = (lo + hi) / 2;
            long needed = 1;
            long load = 0;
            for (long p : pages) {
                if (load + p > mid) {
                    needed++;
                    load = 0;
                }
                load += p;
            }
            if (needed <= students) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        System.out.println(allocateBooks(new long[]{12L, 34L, 67L, 90L}, 2L));
    }
}
