import java.util.Arrays;

public class Main {
    // O(n) time, O(1) extra space
    static long[] twoSingleNumbers(long[] nums) {
        long xorAll = 0;
        for (long x : nums) {
            xorAll ^= x;
        }
        long low = xorAll & -xorAll;
        long a = 0, b = 0;
        for (long x : nums) {
            if ((x & low) != 0) {
                a ^= x;
            } else {
                b ^= x;
            }
        }
        return new long[]{Math.min(a, b), Math.max(a, b)};
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(twoSingleNumbers(new long[]{1L, 2L, 1L, 3L, 2L, 5L})));
    }
}
