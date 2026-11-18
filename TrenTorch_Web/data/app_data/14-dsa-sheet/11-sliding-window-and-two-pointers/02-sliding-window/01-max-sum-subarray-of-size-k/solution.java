public class Main {
    // O(n) time, O(1) space
    static long maxSumK(long[] nums, long k) {
        int kk = (int) k;
        long total = 0;
        for (int i = 0; i < kk; i++) {
            total += nums[i];
        }
        long best = total;
        for (int i = kk; i < nums.length; i++) {
            total += nums[i] - nums[i - kk];
            best = Math.max(best, total);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(maxSumK(new long[]{2L, 1L, 5L, 1L, 3L, 2L}, 3L));
    }
}
