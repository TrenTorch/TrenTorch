public class Main {
    // O(log n) time, O(1) space
    static long lowerBound(long[] nums, long target) {
        int lo = 0, hi = nums.length;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        System.out.println(lowerBound(new long[]{1L, 2L, 2L, 2L, 5L}, 2L));
    }
}
