import java.math.BigInteger;

public class Main {
    // O(k * log^2 n) time for k fixed bases, O(1) space (deterministic Miller-Rabin for n < 3.3e24)
    static boolean isPrime(long n) {
        if (n < 2) {
            return false;
        }
        long[] small = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
        for (long p : small) {
            if (n % p == 0) {
                return n == p;
            }
        }
        long d = n - 1;
        int s = 0;
        while (d % 2 == 0) {
            d /= 2;
            s++;
        }
        for (long a : small) {
            long x = powMod(a, d, n);
            if (x == 1 || x == n - 1) {
                continue;
            }
            boolean composite = true;
            for (int r = 0; r < s - 1; r++) {
                x = mulMod(x, x, n);
                if (x == n - 1) {
                    composite = false;
                    break;
                }
            }
            if (composite) {
                return false;
            }
        }
        return true;
    }

    static long mulMod(long a, long b, long m) {
        return BigInteger.valueOf(a)
                .multiply(BigInteger.valueOf(b))
                .mod(BigInteger.valueOf(m))
                .longValue();
    }

    static long powMod(long base, long exp, long mod) {
        long result = 1 % mod;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1) == 1) {
                result = mulMod(result, base, mod);
            }
            base = mulMod(base, base, mod);
            exp >>= 1;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(isPrime(97L));
    }
}
