public class Main {
    // O(n) time, O(1) space
    static long missingNumber(long[] nums) {
        long n = nums.length;
        long total = 0;
        for (long x : nums) {
            total += x;
        }
        return n * (n + 1) / 2 - total;
    }

    public static void main(String[] args) {
        System.out.println(missingNumber(new long[]{3L, 0L, 1L}));
    }
}
