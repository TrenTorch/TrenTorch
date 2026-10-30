import java.util.Arrays;

public class Main {
    // O(n) time, O(n) space
    static long[] sortedSquares(long[] nums) {
        int n = nums.length;
        long[] out = new long[n];
        int left = 0, right = n - 1;
        for (int i = n - 1; i >= 0; i--) {
            long leftVal = nums[left];
            long rightVal = nums[right];
            if (Math.abs(leftVal) > Math.abs(rightVal)) {
                out[i] = leftVal * leftVal;
                left++;
            } else {
                out[i] = rightVal * rightVal;
                right--;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(sortedSquares(new long[]{-4L, -1L, 0L, 3L, 10L})));
    }
}
