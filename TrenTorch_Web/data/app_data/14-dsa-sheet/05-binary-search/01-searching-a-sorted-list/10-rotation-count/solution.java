public class Main {
    // O(log n) time, O(1) space
    static long rotationCount(long[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] > nums[hi]) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return lo;
    }

    public static void main(String[] args) {
        System.out.println(rotationCount(new long[]{3L, 4L, 5L, 1L, 2L}));
    }
}
