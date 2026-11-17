public class Main {
    // O(n) time, O(1) space
    static long minSubarrayLen(long target, long[] nums) {
        int n = nums.length;
        long best = n + 1L;
        long total = 0L;
        int left = 0;
        for (int right = 0; right < n; right++) {
            total += nums[right];
            while (total >= target) {
                long len = right - left + 1L;
                if (len < best) best = len;
                total -= nums[left];
                left++;
            }
        }
        return best <= n ? best : 0L;
    }

    public static void main(String[] args) {
        System.out.println(minSubarrayLen(7L, new long[]{2L, 3L, 1L, 2L, 4L, 3L}));
    }
}
