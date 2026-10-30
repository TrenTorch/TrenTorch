import java.util.Arrays;

public class Main {
    // O(n) time, O(n) space
    static long[] sortColors(long[] nums) {
        int zeros = 0;
        int ones = 0;
        int twos = 0;
        for (long x : nums) {
            if (x == 0) {
                zeros++;
            } else if (x == 1) {
                ones++;
            } else if (x == 2) {
                twos++;
            }
        }
        long[] out = new long[zeros + ones + twos];
        int idx = 0;
        for (int i = 0; i < zeros; i++) {
            out[idx++] = 0L;
        }
        for (int i = 0; i < ones; i++) {
            out[idx++] = 1L;
        }
        for (int i = 0; i < twos; i++) {
            out[idx++] = 2L;
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(sortColors(new long[]{2L, 0L, 2L, 1L, 1L, 0L})));
    }
}
