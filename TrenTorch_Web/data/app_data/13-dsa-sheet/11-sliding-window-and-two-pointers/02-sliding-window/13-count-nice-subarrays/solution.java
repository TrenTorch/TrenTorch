public class Main {
    // O(n) time, O(1) space
    static long numberOfSubarrays(long[] nums, long k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    private static long atMost(long[] nums, long m) {
        if (m < 0) {
            return 0;
        }
        long odd = 0;
        int left = 0;
        long total = 0;
        for (int right = 0; right < nums.length; right++) {
            odd += nums[right] % 2;
            while (odd > m) {
                odd -= nums[left] % 2;
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(numberOfSubarrays(new long[]{1L, 1L, 2L, 1L, 1L}, 3L));
    }
}
