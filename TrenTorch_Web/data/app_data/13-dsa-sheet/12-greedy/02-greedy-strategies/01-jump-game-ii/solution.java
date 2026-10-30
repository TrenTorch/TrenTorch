public class Main {
    // O(n) time, O(1) space
    static long minJumps(long[] nums) {
        int n = nums.length;
        if (n <= 1) {
            return 0;
        }
        long jumps = 0;
        long end = 0;
        long far = 0;
        for (int i = 0; i < n - 1; i++) {
            far = Math.max(far, i + nums[i]);
            if (i == far) {
                return -1;
            }
            if (i == end) {
                jumps++;
                end = far;
                if (end >= n - 1) {
                    break;
                }
            }
        }
        return end >= n - 1 ? jumps : -1;
    }

    public static void main(String[] args) {
        System.out.println(minJumps(new long[]{2L, 3L, 1L, 1L, 4L}));
    }
}
