public class Main {
    // O(log n) time, O(1) space
    static long singleNonDuplicate(long[] nums) {
        int lo = 0;
        int hi = nums.length - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (mid % 2 == 1) {
                mid--;
            }
            if (nums[mid] == nums[mid + 1]) {
                lo = mid + 2;
            } else {
                hi = mid;
            }
        }
        return nums[lo];
    }

    public static void main(String[] args) {
        System.out.println(singleNonDuplicate(new long[]{1L, 1L, 2L, 3L, 3L, 4L, 4L, 8L, 8L}));
    }
}
