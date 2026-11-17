public class Main {
    // O(log n) time, O(1) space
    static long rotatedMinimum(long[] nums) {
        int lo = 0;
        int hi = nums.length - 1;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (nums[mid] > nums[hi]) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return nums[lo];
    }

    public static void main(String[] args) {
        System.out.println(rotatedMinimum(new long[]{4L, 5L, 6L, 7L, 0L, 1L, 2L}));
    }
}
