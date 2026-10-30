public class Main {
    // O(n) time, O(1) space
    static long singleNumber(long[] nums) {
        long result = 0;
        for (long num : nums) {
            result ^= num;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(singleNumber(new long[]{4L, 1L, 2L, 1L, 2L}));
    }
}
