public class Main {
    // O(n) time, O(1) space
    static long longestOnes(long[] nums, long k) {
        long zeros = 0;
        int left = 0;
        long best = 0;
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == 0) {
                zeros++;
            }
            while (zeros > k) {
                if (nums[left] == 0) {
                    zeros--;
                }
                left++;
            }
            long currentLength = right - left + 1;
            if (currentLength > best) {
                best = currentLength;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestOnes(new long[]{1L, 1L, 1L, 0L, 0L, 0L, 1L, 1L, 1L, 1L, 0L}, 2L));
    }
}
