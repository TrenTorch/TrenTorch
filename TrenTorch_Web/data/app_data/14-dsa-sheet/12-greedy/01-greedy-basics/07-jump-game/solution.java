public class Main {
    // O(n) time, O(1) space
    static boolean canJump(long[] nums) {
        long far = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > far) {
                return false;
            }
            far = Math.max(far, i + nums[i]);
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(canJump(new long[]{2L, 3L, 1L, 1L, 4L}));
    }
}
