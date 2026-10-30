public class Main {
    // O(n log M) time, O(1) space where M = max(nums)
    static long smallestDivisor(long[] nums, long threshold) {
        long lo = 1;
        long hi = 0;
        for (long x : nums) {
            if (x > hi) hi = x;
        }
        while (lo < hi) {
            long mid = (lo + hi) / 2;
            long sum = 0;
            for (long x : nums) {
                sum += (x + mid - 1) / mid;
                if (sum > threshold) break;
            }
            if (sum <= threshold) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        System.out.println(smallestDivisor(new long[]{1L, 2L, 5L, 9L}, 6L));
    }
}
