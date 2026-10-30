public class Main {
    // O(log n) time, O(1) space
    static long mountainPeak(long[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] < nums[mid + 1]) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        System.out.println(mountainPeak(new long[]{1L, 3L, 5L, 4L, 2L}));
    }
}
