import java.math.BigInteger;

public class Main {
    // O(n * S) time, O(S) space where S is sum of nums
    static boolean canPartition(long[] nums) {
        long total = 0;
        for (long num : nums) {
            total += num;
        }
        if ((total & 1) != 0) {
            return false;
        }
        int target = (int) (total / 2);
        BigInteger bits = BigInteger.ONE;
        for (long x : nums) {
            int shift = (int) x;
            bits = bits.or(bits.shiftLeft(shift));
        }
        return bits.testBit(target);
    }

    public static void main(String[] args) {
        System.out.println(canPartition(new long[]{1L, 5L, 11L, 5L}));
    }
}
