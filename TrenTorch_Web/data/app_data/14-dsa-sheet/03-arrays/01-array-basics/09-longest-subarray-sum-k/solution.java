public class Main {
    // O(n) time, O(1) space
    static long longestSubarraySumK(long[] nums, long k) {
        long best = 0;
        long total = 0;
        int left = 0;
        for (int right = 0; right < nums.length; right++) {
            total += nums[right];
            while (total > k && left <= right) {
                total -= nums[left];
                left++;
            }
            if (total == k) {
                long currentLength = right - left + 1;
                if (currentLength > best) {
                    best = currentLength;
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestSubarraySumK(new long[]{1L, 2L, 3L, 1L, 1L, 1L, 1L}, 3L));
    }
}
