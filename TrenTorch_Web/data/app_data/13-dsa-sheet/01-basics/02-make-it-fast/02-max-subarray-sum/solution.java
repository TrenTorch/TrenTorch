public class Main {
    // O(n) time, O(1) space
    static long maxSubarraySum(long[] nums) {
        long best = nums[0];
        long cur = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            best = Math.max(best, cur);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(maxSubarraySum(new long[]{-2L, 1L, -3L, 4L, -1L, 2L, 1L, -5L, 4L}));
    }
}
