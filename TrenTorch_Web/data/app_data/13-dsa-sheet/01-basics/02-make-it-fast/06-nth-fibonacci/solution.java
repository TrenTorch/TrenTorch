import java.math.BigInteger;

public class Main {
    // O(log n) time, O(n) space for result (n = input)
    static BigInteger nthFibonacci(long n) {
        return fib(n)[0];
    }

    private static BigInteger[] fib(long k) {
        if (k == 0) {
            return new BigInteger[]{BigInteger.ZERO, BigInteger.ONE};
        }
        BigInteger[] ab = fib(k >> 1);
        BigInteger a = ab[0];
        BigInteger b = ab[1];
        BigInteger c = a.multiply(b.shiftLeft(1).subtract(a));
        BigInteger d = a.multiply(a).add(b.multiply(b));
        if ((k & 1) == 1) {
            return new BigInteger[]{d, c.add(d)};
        } else {
            return new BigInteger[]{c, d};
        }
    }

    public static void main(String[] args) {
        System.out.println(nthFibonacci(10L));
    }
}
