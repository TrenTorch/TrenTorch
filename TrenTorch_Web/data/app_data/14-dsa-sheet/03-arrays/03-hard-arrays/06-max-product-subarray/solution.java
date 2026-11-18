import java.util.Arrays;

public class Main {
    // O(n) time, O(1) space
    static long maxProductSubarray(long[] nums) {
        long best = nums[0];
        long hi = nums[0];
        long lo = nums[0];
        for (int i = 1; i < nums.length; i++) {
            long x = nums[i];
            long hiX = hi * x;
            long loX = lo * x;
            long newHi = Math.max(x, Math.max(hiX, loX));
            long newLo = Math.min(x, Math.min(hiX, loX));
            hi = newHi;
            lo = newLo;
            if (hi > best) best = hi;
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(maxProductSubarray(new long[]{2L, 3L, -2L, 4L}));
    }
}
