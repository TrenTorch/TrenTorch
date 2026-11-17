public class Main {
    // O(n) time, O(1) space
    static long robCircle(long[] nums) {
        if (nums.length == 0) return 0;
        if (nums.length == 1) return nums[0];
        return Math.max(line(nums, 1, nums.length), line(nums, 0, nums.length - 1));
    }

    static long line(long[] nums, int start, int end) {
        long skip = 0, take = 0;
        for (int i = start; i < end; i++) {
            long x = nums[i];
            long newSkip = Math.max(skip, take);
            long newTake = skip + x;
            skip = newSkip;
            take = newTake;
        }
        return Math.max(skip, take);
    }

    public static void main(String[] args) {
        System.out.println(robCircle(new long[]{2L, 3L, 2L}));
    }
}
