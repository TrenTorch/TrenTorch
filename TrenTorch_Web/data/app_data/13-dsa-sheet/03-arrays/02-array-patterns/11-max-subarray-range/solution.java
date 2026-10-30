public class Main {
    // O(n) time, O(1) space
    static long[] maxSubarrayRange(long[] nums) {
        long bestSum = nums[0];
        int bestStart = 0;
        int bestEnd = 0;
        long current = nums[0];
        int begin = 0;
        for (int i = 1; i < nums.length; i++) {
            if (current < 0) {
                current = nums[i];
                begin = i;
            } else {
                current += nums[i];
            }
            if (current > bestSum) {
                bestSum = current;
                bestStart = begin;
                bestEnd = i;
            }
        }
        return new long[]{bestSum, bestStart, bestEnd};
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(maxSubarrayRange(new long[]{-2L, 1L, -3L, 4L, -1L, 2L, 1L, -5L, 4L})));
    }
}
