public class Main {
    // O(n) time, O(1) space
    static long rob(long[] nums) {
        long skip = 0;
        long take = 0;
        for (long x : nums) {
            long newSkip = Math.max(skip, take);
            take = skip + x;
            skip = newSkip;
        }
        return Math.max(skip, take);
    }

    public static void main(String[] args) {
        System.out.println(rob(new long[]{1L, 2L, 3L, 1L}));
    }
}
