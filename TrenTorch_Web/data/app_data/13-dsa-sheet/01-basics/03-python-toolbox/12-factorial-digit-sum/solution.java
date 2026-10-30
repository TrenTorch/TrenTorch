import java.math.BigInteger;

public class Main {
    // O(n^2 log n) time for building n! as a BigInteger, O(n log n) space
    static long factorialDigitSum(long n) {
        BigInteger f = BigInteger.ONE;
        for (long i = 2; i <= n; i++) {
            f = f.multiply(BigInteger.valueOf(i));
        }
        long sum = 0;
        for (char c : f.toString().toCharArray()) {
            sum += c - '0';
        }
        return sum;
    }

    public static void main(String[] args) {
        System.out.println(factorialDigitSum(10L));
    }
}
