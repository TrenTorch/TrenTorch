import java.util.Arrays;

public class Main {
    // O(n log S) time, O(1) space
    static long shipCapacity(long[] weights, long days) {
        long lo = 0;
        long hi = 0;
        for (long w : weights) {
            if (w > lo) lo = w;
            hi += w;
        }
        while (lo < hi) {
            long mid = (lo + hi) / 2;
            long needed = 1;
            long load = 0;
            for (long w : weights) {
                if (load + w > mid) {
                    needed++;
                    load = 0;
                }
                load += w;
            }
            if (needed <= days) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        System.out.println(shipCapacity(new long[]{1L, 2L, 3L, 4L, 5L, 6L, 7L, 8L, 9L, 10L}, 5L));
    }
}
