public class Main {
    // O(n) time, O(1) space
    static long singleNumberIi(long[] nums) {
        long ones = 0;
        long twos = 0;
        for (long x : nums) {
            ones = (ones ^ x) & ~twos;
            twos = (twos ^ x) & ~ones;
        }
        return ones;
    }

    public static void main(String[] args) {
        System.out.println(singleNumberIi(new long[]{2L, 2L, 3L, 2L}));
    }
}
