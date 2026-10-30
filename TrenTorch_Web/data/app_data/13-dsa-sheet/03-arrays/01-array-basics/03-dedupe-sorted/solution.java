import java.util.Arrays;

public class Main {
    // O(n) time, O(n) space
    static long[] dedupeSorted(long[] nums) {
        if (nums == null || nums.length == 0) {
            return new long[0];
        }
        long[] out = new long[nums.length];
        int outIdx = 0;
        for (long x : nums) {
            if (outIdx == 0 || out[outIdx - 1] != x) {
                out[outIdx++] = x;
            }
        }
        return Arrays.copyOf(out, outIdx);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(dedupeSorted(new long[]{1L, 1L, 2L, 2L, 2L, 3L})));
    }
}
