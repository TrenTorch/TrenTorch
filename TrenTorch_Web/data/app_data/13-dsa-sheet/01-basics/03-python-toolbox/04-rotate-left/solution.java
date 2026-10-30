import java.util.Arrays;

public class Main {
    // O(n) time, O(n) space
    static long[] rotateLeft(long[] nums, long k) {
        if (nums.length == 0) {
            return new long[0];
        }
        int n = nums.length;
        int rot = (int)(k % n);
        long[] result = new long[n];
        System.arraycopy(nums, rot, result, 0, n - rot);
        System.arraycopy(nums, 0, result, n - rot, rot);
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(rotateLeft(new long[]{1L, 2L, 3L, 4L, 5L}, 2L)));
    }
}
