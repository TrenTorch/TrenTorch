public class Main {
    // O(n) time, O(1) space
    static long pivotIndex(long[] nums) {
        long total = 0;
        for (long x : nums) {
            total += x;
        }
        long left = 0;
        for (int i = 0; i < nums.length; i++) {
            long x = nums[i];
            if (left == total - left - x) {
                return i;
            }
            left += x;
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println(pivotIndex(new long[]{1L, 7L, 3L, 6L, 5L, 6L}));
    }
}
