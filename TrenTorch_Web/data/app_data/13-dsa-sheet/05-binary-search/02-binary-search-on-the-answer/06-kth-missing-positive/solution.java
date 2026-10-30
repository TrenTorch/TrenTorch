public class Main {
    // O(log n) time, O(1) space
    static long kthMissingPositive(long[] nums, long k) {
        int lo = 0, hi = nums.length;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (nums[mid] - (mid + 1L) < k) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return lo + k;
    }

    public static void main(String[] args) {
        System.out.println(kthMissingPositive(new long[]{2L, 3L, 4L, 7L, 11L}, 5L));
    }
}
