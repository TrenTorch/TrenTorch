public class Main {
    // O(n) time, O(1) space
    static long wiggleLength(long[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int length = 1;
        int direction = 0;
        for (int i = 1; i < nums.length; i++) {
            long diff = nums[i] - nums[i - 1];
            if (diff > 0 && direction <= 0) {
                length++;
                direction = 1;
            } else if (diff < 0 && direction >= 0) {
                length++;
                direction = -1;
            }
        }
        return length;
    }

    public static void main(String[] args) {
        System.out.println(wiggleLength(new long[]{1L, 7L, 4L, 9L, 2L, 5L}));
    }
}
