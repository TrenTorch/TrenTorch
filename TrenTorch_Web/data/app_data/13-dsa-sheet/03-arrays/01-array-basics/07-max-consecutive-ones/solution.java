public class Main {
    // O(n) time, O(1) space
    static long maxConsecutiveOnes(long[] nums) {
        long best = 0;
        long current = 0;
        for (long x : nums) {
            if (x == 1) {
                current += 1;
                if (current > best) {
                    best = current;
                }
            } else {
                current = 0;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(maxConsecutiveOnes(new long[]{1L, 1L, 0L, 1L, 1L, 1L}));
    }
}
