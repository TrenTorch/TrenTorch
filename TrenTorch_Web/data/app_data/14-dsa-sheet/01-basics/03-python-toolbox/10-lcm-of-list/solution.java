import java.math.BigInteger;

public class Main {
    // O(n * B^2) time for B-bit intermediate values, O(B) space
    // Returns long via longValueExact: throws if the true LCM exceeds 64 bits
    static long lcmOfList(long[] nums) {
        BigInteger result = BigInteger.ONE;
        for (long num : nums) {
            BigInteger b = BigInteger.valueOf(num);
            result = result.divide(result.gcd(b)).multiply(b);
        }
        return result.longValueExact();
    }

    public static void main(String[] args) {
        System.out.println(lcmOfList(new long[]{4L, 6L, 10L}));
    }
}
