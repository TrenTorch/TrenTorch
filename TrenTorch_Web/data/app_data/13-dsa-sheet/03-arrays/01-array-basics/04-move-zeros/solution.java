import java.util.Arrays;

public class Main {
    // O(n) time, O(n) space
    static long[] moveZeros(long[] nums) {
        long[] out = new long[nums.length];
        int idx = 0;
        for (long x : nums) {
            if (x != 0) {
                out[idx++] = x;
            }
        }
        // remaining slots are already 0
        return out;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(moveZeros(new long[]{0L, 1L, 0L, 3L, 12L})));
    }
}
